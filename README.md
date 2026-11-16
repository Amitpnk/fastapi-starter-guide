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
