# secure-alert

Fictional security alert system for receiving, storing and serving security event data originating from devices, such as security cameras.

Built considering an imagined time constraint, limiting the implementation to 3h. Design, framework, library and tool choices reflect the constraint.

## Project setup and running

### Requirements

1. python 3.14 ([download page](https://www.python.org/downloads/))
2. uv package and project manager ([installation instructions](https://docs.astral.sh/uv/getting-started/installation/))
3. (Optional) Task ([installation instructions](https://taskfile.dev/docs/installation)) for easier access to commands, such as for starting the app. If you prefer not to install it, you can run the commands directly, as also given in this README.

### General setup for all workflows

1. Copy `.env.template` to `.env` and add env variable values (example)

```shell
cp .env.template .env
````

```shell
SECRET_KEY="django-insecure-35%=i6j36#oc&_iwx3f4_e9k93lwp7e&af*^gdt=12kxi!*jla"
DEBUG=1
ALLOWED_HOSTS="127.0.0.1,localhost"
```

`SECRET_KEY` is required, while other values are optional (they have defaults).

2. Setup the project and install dependencies with uv.

```shell
uv sync
```

3. Run initial migrations (this creates Django admin user related tables)

```shell
task migrate

# or

uv run manage.py migrate
```

4. Create an admin user (optional; used to create sample data easily, and otherwise manage the application through an interface)

```shell
uv run manage.py createsuperuser --username admin --email admin@example.com
```

### Run local application

Using Task

```shell
task start-app
```

Using the command directly

```shell
uv run manage.py runserver
```

The application will be served at <http://localhost:8000>.

### Lint and format the code

Using Task

```shell
task lint
```

Using the commands directly

```shell
uv run ruff check
uv run ruff format
```

### Create migrations

Run whenever models are created or modified. This includes modifications such as in model field parameters, even for parameters like `help_text`. When in doubt, just run the command and check the output.

Using tax

```shell
task create-migration
```

Using the command directly

```shell
uv run manage.py makemigrations
```

## Troubleshooting

Depending on your operational system, support for JSON columns ([JSON1 extension](https://code.djangoproject.com/wiki/JSON1Extension)) may not be enabled by default in you python's installation. It is, however, included for most systems in modern python versions, including python 3.14.

If you face any sqlite, model or DB-related JSON errors:

1. Double check your python version
2. Follow the instructions in the following page: <https://code.djangoproject.com/wiki/JSON1Extension>

## Tool choices

Tools/stack/tech of choice and reasoning for choosing them.

| What | Choice | Why |
| - | - | - |
| Task manager | [Task](https://taskfile.dev/) | Simpler and easier to understand than Makefiles, works as a tool to build, run, etc. |
| Package and project manager | [uv](https://docs.astral.sh/uv/) | Faster than pip and less complicated than poetry, while having more or less the same features, as it derives from poetry |
| Framework | [Django](https://www.djangoproject.com/) and [Django REST framework](https://www.django-rest-framework.org/) (DRF) | Fast and easy to implement, all batteries included; fits well in a 3h deadline, with the caveat of not supporting async programming fully |
| Testing | [pytest](https://docs.pytest.org/en/stable/) | Well-maintained, easier to use than unittest, and comes with good features, such as fixtures, and various plugins |
| Database | [SQLite](https://sqlite.org/index.html) | Easy and light, suitable for a demo; latest versions support JSON columns |

## Improvements to be implemented

- Configure a test workflow with a separate DB. For the sake of simplicity, this app uses the same DB for all workflows - running the app, testing.
- Create docker image and configure running app, tests, etc. in containers.
- Add token-based authentication to `GET` endpoints and device-compatible authentication (specifics to be figured out) to `POST` endpoint.
- Replace SQLite with [PostgreSQL](https://www.postgresql.org/) for robustness in production, specially the speed of reads (including JSON columns).
- Modify choice of libs/frameworks to be able to use async fully. Options: remove DRF use (Django by itself supports async); replace Django and DRF with [FastAPI](https://fastapi.tiangolo.com/); or customize by overriding and rewriting DRF view code (the blocker for full async use).
- Use [pre-commit](https://pre-commit.com/), or similar, to check, link and format code before each commit.
- Add logging and metrics.

## Generative AI use disclaimer

The project was coded manually in order to accurately represent the author's raw coding skils. No form of agentic coding was used (claude, codex, copilot, etc.).

Most search engines, including the one used by the author ([DuckDuckGo](https://duckduckgo.com)), implement AI generated responses, now; those have been consulted while doing research for the project implementation, specially when debugging errors.
