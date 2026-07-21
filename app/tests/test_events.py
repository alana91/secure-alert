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


@pytest.mark.django_db
def test_summary_most_active_device(client: APIClient):
    baker.make(Event, device_id="very_active", _quantity=3)
    baker.make(Event, device_id="not_so_active_1", _quantity=1)
    baker.make(Event, device_id="not_so_active_2", _quantity=2)
    response = client.get("/events/summary/")
    assert response.status_code == 200
    assert response.data["total_events"] == 6
    assert response.data["most_active_device"] == "very_active"


@pytest.mark.django_db
def test_summary_by_severity(client: APIClient):
    baker.make(Event, severity="low", _quantity=2)
    baker.make(Event, severity="medium", _quantity=4)
    baker.make(Event, severity="high", _quantity=8)
    response = client.get("/events/summary/")
    assert response.status_code == 200
    assert response.data["total_events"] == 14
    assert response.data["by_severity"]["low"] == 2
    assert response.data["by_severity"]["medium"] == 4
    assert response.data["by_severity"]["high"] == 8


@pytest.mark.django_db
def test_summary_by_event_type(client: APIClient):
    baker.make(Event, event_type="motion_detected", _quantity=2)
    baker.make(Event, event_type="intrusion_alert", _quantity=4)
    baker.make(Event, event_type="camera_offline", _quantity=8)
    response = client.get("/events/summary/")
    assert response.status_code == 200
    assert response.data["total_events"] == 14
    assert response.data["by_event_type"]["motion_detected"] == 2
    assert response.data["by_event_type"]["intrusion_alert"] == 4
    assert response.data["by_event_type"]["camera_offline"] == 8


@pytest.mark.django_db
def test_summary_high_severity_rate(client: APIClient):
    baker.make(Event, severity="low", _quantity=1)
    baker.make(Event, severity="medium", _quantity=1)
    baker.make(Event, severity="high", _quantity=2)
    response = client.get("/events/summary/")
    assert response.status_code == 200
    assert response.data["high_severity_rate"] == 0.5


@pytest.mark.django_db
def test_summary_with_zero_events(client: APIClient):
    response = client.get("/events/summary/")
    assert response.status_code == 200
    assert response.data["total_events"] == 0
    assert response.data["most_active_device"] == ""
    assert response.data["by_severity"]["low"] == 0
    assert response.data["by_severity"]["medium"] == 0
    assert response.data["by_severity"]["high"] == 0
    assert response.data["by_event_type"]["motion_detected"] == 0
    assert response.data["by_event_type"]["intrusion_alert"] == 0
    assert response.data["by_event_type"]["camera_offline"] == 0
    assert response.data["high_severity_rate"] == 0.0
