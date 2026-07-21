import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from app.models import Event


@pytest.fixture
def valid_event_data() -> dict[str, str | dict]:
    return {
        "device_id": "camera-1",
        "event_type": "motion_detected",
        "severity": "low",
        "timestamp": "2026-07-21T11:01:36.878000Z",
        "metadata": {"some": "meta"},
    }


@pytest.mark.django_db
def test_create_event(client: APIClient, valid_event_data: dict[str, str | dict]):
    response = client.post("/events/", valid_event_data, format="json")
    assert response.status_code == 201
    result = response.data
    assert result["id"] > 0
    assert result["event_type"] == "motion_detected"
    assert result["severity"] == "low"
    assert result["timestamp"] == "2026-07-21T11:01:36.878000Z"
    assert result["metadata"] == {"some": "meta"}


@pytest.mark.django_db
def test_list_events(client: APIClient):
    baker.make(Event, _quantity=2)
    response = client.get("/events/")
    assert response.status_code == 200
    assert response.data["total"] == 2
    assert len(response.data["events"]) == 2


@pytest.mark.django_db
@pytest.mark.parametrize("field", ["event_type", "device_id", "severity"])
def test_filter_events(client: APIClient, field: str):
    filtered_event = baker.make(
        Event, device_id="camera-1", event_type="motion_detected", severity="low"
    )
    baker.make(
        Event, device_id="camera-2", event_type="intrusion_alert", severity="high"
    )
    response = client.get("/events/", data={field: getattr(filtered_event, field)})
    assert response.status_code == 200
    assert response.data["total"] == 1
    assert len(response.data["events"]) == 1
    assert response.data["events"][0]["id"] == filtered_event.id


@pytest.mark.django_db
def test_filter_events_by_timestamp(client: APIClient):
    filter_from = "2026-07-21T11:01:01Z"
    filter_to = "2026-07-21T11:01:02Z"
    baker.make(Event, timestamp="2026-07-21T11:01:00Z")
    filtered_event_from = baker.make(Event, timestamp=filter_from)
    filtered_event_to = baker.make(Event, timestamp=filter_to)
    baker.make(Event, timestamp="2026-07-21T11:01:03Z")
    response = client.get(
        "/events/", data={"timestamp_from": filter_from, "timestamp_to": filter_to}
    )
    assert response.status_code == 200
    assert response.data["total"] == 2
    assert len(response.data["events"]) == 2
    ids = [result["id"] for result in response.data["events"]]
    assert filtered_event_from.id in ids
    assert filtered_event_to.id in ids


@pytest.mark.django_db
def test_pagination(client: APIClient):
    baker.make(Event, _quantity=100)
    response = client.get("/events/", data={"page_size": 100})
    assert response.status_code == 200
    assert len(response.data["events"]) == 100
    response = client.get("/events/")
    assert response.status_code == 200
    assert len(response.data["events"]) == 20
