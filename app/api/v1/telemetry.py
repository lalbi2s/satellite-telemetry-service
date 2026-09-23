from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.telemetry import TelemetryPacketCreate, TelemetryPacketResponse
from app.models.telemetry import TelemetryRecord
from app.services.anomaly_detection import detect_severity

router = APIRouter()


@router.post("/telemetry", response_model=TelemetryPacketResponse)
async def create_telemetry(
    packet: TelemetryPacketCreate,
    db: AsyncSession = Depends(get_db),
):
    severity = detect_severity(packet.metric_name, packet.value)

    record = TelemetryRecord(
        satellite_id=packet.satellite_id,
        subsystem=packet.subsystem,
        metric_name=packet.metric_name,
        value=packet.value,
        unit=packet.unit,
        timestamp=packet.timestamp,
        severity=severity,
    )

    db.add(record)
    await db.commit()
    await db.refresh(record)

    return record
