import pytest


@pytest.mark.asyncio
async def test_create_telemetry_nominal(client):
    payload = {
        "satellite_id": "AEROLAB-SAT-01",
        "subsystem": "EPS",
        "metric_name": "temperature",
        "value": 20.0,
        "unit": "C",
    }

    response = await client.post("/api/v1/telemetry", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["severity"] == "NOMINAL"
    assert data["satellite_id"] == "AEROLAB-SAT-01"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_telemetry_critical(client):
    payload = {
        "satellite_id": "AEROLAB-SAT-01",
        "subsystem": "EPS",
        "metric_name": "temperature",
        "value": 95.0,
        "unit": "C",
    }

    response = await client.post("/api/v1/telemetry", json=payload)

    assert response.status_code == 200
    assert response.json()["severity"] == "CRITICAL"


@pytest.mark.asyncio
async def test_create_telemetry_rejects_invalid_battery_voltage(client):
    payload = {
        "satellite_id": "AEROLAB-SAT-01",
        "subsystem": "EPS",
        "metric_name": "battery_voltage",
        "value": 999.0,
        "unit": "V",
    }

    response = await client.post("/api/v1/telemetry", json=payload)

    assert response.status_code == 422
