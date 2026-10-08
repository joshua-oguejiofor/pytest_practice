# Pytest Practice: Async Todo Application

An application built for mastering automated asynchronous testing for FastAPI applications using `pytest`, `httpx`, and `SQLAlchemy`.

---

## Tech Stack
* **Framework:** [FastAPI]
* **Database:** SQLite with [aiosqlite]
* **ORM:** [SQLAlchemy 2.0] (Async engine)
* **Migrations:** [Alembic]
* **Testing:** [pytest], [pytest-asyncio], [httpx]
* **ASGI Server:** [uvicorn]

---

## Project Directory Structure

```text
app/
├── app/
│   ├── alembic/              # Database migrations directory
│   ├── alembic.ini           # Alembic configuration
│   ├── app_logger.py         # Application logger configuration
│   ├── database.py           # Database connection and Session setup
│   ├── exception.py          # Custom HTTP & application exceptions
│   ├── __init__.py
│   ├── main.py               # FastAPI application instance
│   ├── model.py              # SQLAlchemy ORM database models
│   ├── route.py              # API endpoint routes
│   └── schema.py             # Pydantic data schemas
├── tests/
│   ├── conftest.py           # Pytest async fixtures (engine, sessions, client)
│   ├── __init__.py
│   └── test_main.py          # Async API test functions
├── pytest.ini                # Pytest configuration file
├── requirements.txt          # Dependencies list
└── README.md                 # Project documentation
```


# Environment Setup & Installation
1. Prerequisites
Ensure you have Python 3.10+ installed on your machine.

2. Create and Activate Virtual Environment

```Bash
# Navigate to project directory
cd app

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux / macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

3. Install Dependencies

```Bash
pip install --upgrade pip
pip install -r requirements.txt

# Run using uvicorn from the app module
uvicorn app.main:app --reload
```

The server will be available @ http://127.0.0.1:800:

Interactive API Docs (Swagger): http://127.0.0.1:8000/docs

ReDoc Documentation: http://127.0.0.1:8000/redoc

# Running Tests
Tests use pytest-asyncio and httpx.AsyncClient connected to an isolated test database (testdb.db) using transaction rollbacks.

Execute All Tests
From the directory containing pytest.ini, run:

```Bash
python -m pytest

Useful Test Commands

# Run with verbose output (shows individual test names)
python -m pytest -v

# Run with stdout prints visible in console
python -m pytest -s

# Stop on first failure
python -m pytest -x

# Run a specific test file
python -m pytest tests/test_main.py
```

# Author
**Joshua Oguejiofor**