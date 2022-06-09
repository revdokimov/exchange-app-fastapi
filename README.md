# Exchange data test project with FastAPI

It uses alembic and asyncio databases library.

History data avaialable via /exchangerate/history/ endpoint with optional start_date and end_date filters.

Rate for current date available via /exchangerate/rate/ endpoint.

Docs at /docs and /redoc as usual.

Starts on port 8080 via docker compose by default.