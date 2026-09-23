# Satellite Telemetry Service

FastAPI micro-service for ingesting and monitoring satellite telemetry data (temperature, battery voltage, etc.), with automatic anomaly detection.

## Overview

Simulates the collection of measurements from satellite subsystems (EPS, ADCS, PAYLOAD, TTC), validates them, automatically classifies their severity (NOMINAL / WARNING / CRITICAL), and stores them.

Built as part of a hands-on deep dive into the Python stack commonly used in satellite software environments (FastAPI, Pydantic, SQLAlchemy).

## Tech Stack

- **API**: FastAPI
- **Validation**: Pydantic v2
- **Database**: SQLAlchemy (async) + SQLite
- **Testing**: pytest, pytest-asyncio, httpx

## Architecture

app/
├── core/ # Configuration (environment variables, thresholds)
├── schemas/ # Pydantic validation contracts (API input/output)
├── models/ # SQLAlchemy models (database structure)
├── db/ # Database connection and sessions
├── services/ # Business logic (anomaly detection)
└── api/ # FastAPI routes

tests/ # Unit and integration tests


## Running Locally

1. Clone the repo and set up a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Copy the environment file:
```bash
cp .env.example .env
```

3. Start the server:
```bash
uvicorn app.main:app --reload
```

4. Open the interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Running Tests

```bash
pytest -v
```

## Example Usage

**Request** — `POST /api/v1/telemetry`
```json
{
  "satellite_id": "AEROLAB-SAT-01",
  "subsystem": "EPS",
  "metric_name": "temperature",
  "value": 90,
  "unit": "C"
}
```

**Response**
```json
{
  "id": 1,
  "satellite_id": "AEROLAB-SAT-01",
  "subsystem": "EPS",
  "metric_name": "temperature",
  "value": 90,
  "unit": "C",
  "severity": "CRITICAL",
  "timestamp": "2026-09-23T20:12:47Z",
  "received_at": "2026-09-23T20:14:37Z"
}
```

## Anomaly Detection

Configurable temperature thresholds (via environment variables) determine severity:
- **NOMINAL**: value within the normal range
- **WARNING**: value close to the limits
- **CRITICAL**: value outside the acceptable physical range

## Roadmap

- Migrate to PostgreSQL
- Containerize with Docker / Docker Compose
- Manage schema migrations with Alembic
