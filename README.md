# fastapi-starter-guide

A minimal FastAPI app with a simple in-memory CRUD API for items.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)

uv reads `.python-version` and downloads Python 3.12 automatically if it isn't installed.

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup

```bash
uv sync
```

This creates `.venv` and installs the exact versions pinned in `uv.lock`.

## Run

```bash
uv run fastapi dev main.py
```

The API runs at http://127.0.0.1:8000 with auto-reload. For production, use `uv run fastapi run main.py`.

## Create This Project From Scratch

Follow these steps to build a project like this one from an empty folder.

### 1. Install uv (one time only)

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen the terminal, then check it worked with `uv --version`.

### 2. Create the project

```bash
mkdir fastapi-demo
cd fastapi-demo
uv init --python 3.12
```

This creates `pyproject.toml`, `.python-version`, `README.md`, `.gitignore`, and a sample `main.py`. It also starts a git repository if you aren't already in one.

> **Important:** don't name the folder `fastapi`. `uv init` names the project after its folder, and uv won't let a project depend on a package with its own name. See [Troubleshooting](#troubleshooting).

### 3. Add FastAPI

```bash
uv add "fastapi[standard]"
```

This downloads Python 3.12 if you don't have it, creates `.venv`, installs FastAPI and uvicorn, adds FastAPI to `pyproject.toml`, and writes `uv.lock`.

### 4. Write the app

Replace the contents of `main.py` with:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}
```

Then add more endpoints as you need them. The `/items` endpoints in this repo's [`main.py`](main.py) are a full working example.

### 5. Run it

```bash
uv run fastapi dev main.py
```

- API: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs

The server restarts on its own whenever you save a file. Press `Ctrl+C` to stop it.

### 6. Commit

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

- **Rename the project.** In `pyproject.toml`, change `name = "fastapi"` to another name, such as `name = "fastapi-demo"`, then run `uv add "fastapi[standard]"` again.
- **Pick a different name when you create it.** Run `uv init --name fastapi-demo --python 3.12`, or use a folder with a different name.

For the same reason, don't name your project or any of your own files after a package you install. For example, a `fastapi.py` in the folder would be imported instead of the real FastAPI.

## Managing Dependencies

```bash
uv add <package>       # add a dependency
uv remove <package>    # remove a dependency
uv lock --upgrade      # upgrade locked versions
```

## API Docs

FastAPI generates interactive docs automatically:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Endpoints

| Method | Path               | Description         |
|--------|--------------------|---------------------|
| GET    | `/`                | Welcome message     |
| GET    | `/health`          | Health check        |
| GET    | `/items`           | List all items      |
| GET    | `/items/{item_id}` | Get one item        |
| POST   | `/items`           | Create an item      |
| PUT    | `/items/{item_id}` | Replace an item     |
| DELETE | `/items/{item_id}` | Delete an item      |

## Example Requests

```bash
# Create an item
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99}'

# List items
curl http://127.0.0.1:8000/items

# Get one item
curl http://127.0.0.1:8000/items/1

# Update an item
curl -X PUT http://127.0.0.1:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop Pro", "price": 1299.99, "in_stock": false}'

# Delete an item
curl -X DELETE http://127.0.0.1:8000/items/1
```

## Notes

Data is stored in memory, so it resets whenever the server restarts.

## License

See [LICENSE](LICENSE).
