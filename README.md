# fastapi-starter-guide

A FastAPI starter project with a small CRUD API for items. The code is split into layers and grouped by feature, so the app can grow without turning into one big file.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

uv reads `.python-version` and downloads Python 3.12 automatically if it isn't installed.

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Quick Start

```bash
uv sync                          # create .venv and install pinned dependencies
uv run fastapi dev app/main.py   # start the dev server with auto-reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

For production, use `uv run fastapi run app/main.py`.

## Run Tests

```bash
uv run pytest
```

## Project Structure

```
fastapi-starter-guide/
├── app/
│   ├── main.py              # creates the app, registers routers and error handlers
│   ├── core/
│   │   └── config.py        # settings loaded from environment variables
│   └── items/               # everything for the "items" feature
│       ├── router.py        # HTTP endpoints
│       ├── schemas.py       # request and response models
│       ├── service.py       # business logic
│       ├── repository.py    # data storage
│       ├── dependencies.py  # wires the repository and service together
│       └── exceptions.py    # errors for this feature
├── tests/
│   └── test_items.py
├── pyproject.toml           # project metadata and dependencies
├── uv.lock                  # exact pinned versions (commit this)
└── .python-version          # Python version uv uses
```

## Architecture

Each request passes through layers that each have one job:

```
Request → Router → Service → Repository → Storage
            ↑
         Schemas validate input and shape output
```

| Layer | File | Job | Knows about |
|---|---|---|---|
| **Router** | `router.py` | Receive the HTTP request, call the service, return the response | HTTP and schemas |
| **Schemas** | `schemas.py` | Define and validate request and response data | Nothing else |
| **Service** | `service.py` | Business rules, such as "raise an error if the item doesn't exist" | The repository, but not HTTP |
| **Repository** | `repository.py` | Read and write data | Storage only |
| **Dependencies** | `dependencies.py` | Create the service and repository and pass them to routes with `Depends()` | All of the above |

### Why it's built this way

- **Separate schemas for input and output.** `ItemCreate` and `ItemUpdate` describe what clients send, and `ItemRead` describes what the API returns. Clients can't set the `id`, and every route sets `response_model`, so responses are validated and documented.
- **The service doesn't know about HTTP.** It raises `ItemNotFoundError`, and an exception handler in `app/main.py` turns that into a `404`. You can reuse the service from a script or a background job.
- **Dependency injection instead of global variables.** Routes receive the service through `Depends()`. Tests use `app.dependency_overrides` to give every test its own empty repository.
- **The storage can be swapped.** Data lives in memory for now. To use a database, write a repository class with the same methods and return it from `get_item_repository()`. The router and service don't change.
- **Grouped by feature.** All the code for items lives in `app/items/`. To add a feature, add another folder.
- **Versioned API.** Item routes are under `/api/v1`, so a future `/api/v2` won't break existing clients.

### Adding a new feature

For example, to add `users`:

1. Copy `app/items/` to `app/users/` and rename the classes and schemas.
2. Register the router in `app/main.py`:
   ```python
   from app.users.router import router as users_router
   app.include_router(users_router, prefix=settings.api_prefix)
   ```
3. Add `tests/test_users.py`.

## Configuration

Settings are defined in `app/core/config.py` and can be overridden with environment variables or a `.env` file in the project root:

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `FastAPI Starter` | Title shown in the docs |
| `APP_VERSION` | `1.0.0` | Version shown in the docs |
| `API_PREFIX` | `/api/v1` | Prefix for feature routes |
| `DEBUG` | `false` | Enable FastAPI debug mode |

Example `.env`:

```env
APP_NAME=My API
DEBUG=true
```

`.env` is already in `.gitignore`, so secrets stay out of git.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/api/v1/items` | List all items |
| GET | `/api/v1/items/{item_id}` | Get one item |
| POST | `/api/v1/items` | Create an item |
| PUT | `/api/v1/items/{item_id}` | Replace an item |
| DELETE | `/api/v1/items/{item_id}` | Delete an item |

Validation rules: `name` must be 1 to 100 characters, `price` must be greater than 0, and `in_stock` defaults to `true`. Invalid input returns `422`, and a missing item returns `404`.

## Example Requests

```bash
# Create an item
curl -X POST http://127.0.0.1:8000/api/v1/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99}'

# List items
curl http://127.0.0.1:8000/api/v1/items

# Get one item
curl http://127.0.0.1:8000/api/v1/items/1

# Update an item
curl -X PUT http://127.0.0.1:8000/api/v1/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop Pro", "price": 1299.99, "in_stock": false}'

# Delete an item
curl -X DELETE http://127.0.0.1:8000/api/v1/items/1
```

> **Windows PowerShell:** `curl` there is an alias for a different command. Use `curl.exe` instead, or try the requests in Swagger UI at `/docs`.

Data is stored in memory, so it resets whenever the server restarts.

## Managing Dependencies

```bash
uv add <package>          # add a dependency
uv add --dev <package>    # add a dev-only dependency (for example, pytest)
uv remove <package>       # remove a dependency
uv lock --upgrade         # upgrade locked versions
```

## Create This Project From Scratch

Follow these steps to build a project like this one from an empty folder.

### 1. Install uv (one time only)

See [Requirements](#requirements). Close and reopen the terminal afterwards, then check it worked with `uv --version`.

### 2. Create the project

```bash
mkdir fastapi-demo
cd fastapi-demo
uv init --python 3.12
```

This creates `pyproject.toml`, `.python-version`, `README.md`, `.gitignore`, and a sample `main.py`. It also starts a git repository if you aren't already in one.

> **Important:** don't name the folder `fastapi`. `uv init` names the project after its folder, and uv won't let a project depend on a package with its own name. See [Troubleshooting](#troubleshooting).

### 3. Add dependencies

```bash
uv add "fastapi[standard]" pydantic-settings
uv add --dev pytest
```

This downloads Python 3.12 if you don't have it, creates `.venv`, installs the packages, adds them to `pyproject.toml`, and writes `uv.lock`.

### 4. Create the folder structure

Delete the sample `main.py`, then create the package folders. Each folder needs an empty `__init__.py`.

```bash
# macOS / Linux
mkdir -p app/core app/items tests
touch app/__init__.py app/core/__init__.py app/items/__init__.py tests/__init__.py
```

```powershell
# Windows (PowerShell)
mkdir app\core, app\items, tests
ni app\__init__.py, app\core\__init__.py, app\items\__init__.py, tests\__init__.py
```

### 5. Write the code, one layer at a time

Write the files in this order, so each one only imports files that already exist. Use this repo's files as the reference.

1. `app/core/config.py`: settings
2. `app/items/schemas.py`: data models
3. `app/items/exceptions.py`: errors
4. `app/items/repository.py`: storage
5. `app/items/service.py`: business logic
6. `app/items/dependencies.py`: wiring
7. `app/items/router.py`: endpoints
8. `app/main.py`: the app itself
9. `tests/test_items.py`: tests

### 6. Run and test

```bash
uv run fastapi dev app/main.py
uv run pytest
```

The dev server restarts on its own whenever you save a file. Press `Ctrl+C` to stop it.

### 7. Commit

```bash
git add .
git commit -m "Add FastAPI starter app"
```

Commit `uv.lock` too. Anyone who clones the repo can then run `uv sync` and get exactly the same package versions.

## Troubleshooting

### `Requirement name 'fastapi' matches project name 'fastapi'`

```
error: Requirement name `fastapi` matches project name `fastapi`, but self-dependencies are not permitted ...
```

You get this error because the project folder is named `fastapi`, so `uv init` gave the project that name too. You can fix it in either of these ways:

- **Rename the project.** In `pyproject.toml`, change `name = "fastapi"` to another name, such as `name = "fastapi-demo"`, then run the `uv add` command again.
- **Pick a different name when you create it.** Run `uv init --name fastapi-demo --python 3.12`, or use a folder with a different name.

For the same reason, don't name your project or any of your own files after a package you install. For example, a `fastapi.py` in the folder would be imported instead of the real FastAPI.

### `ModuleNotFoundError: No module named 'app'`

Run commands from the project root, which is the folder that contains `pyproject.toml`, and use the path `app/main.py`.

## License

See [LICENSE](LICENSE).
