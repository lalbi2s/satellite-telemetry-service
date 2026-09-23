from datetime import datetime, timezone
from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field, field_validator, ConfigDict

class SubsystemEnum(str, Enum):
    EPS = "EPS"
    ADCS = "ADCS"
    PAYLOAD = "PAYLOAD"
    TTC = "TTC"


class TelemetrySeverity(str, Enum):
    NOMINAL = "NOMINAL"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class TelemetryPacketCreate(BaseModel):
    satellite_id: Annotated[str, Field(min_length=3, max_length=20, examples=["AEROLAB-SAT-01"])]
    subsystem: SubsystemEnum
    metric_name: Annotated[str, Field(min_length=2, max_length=50, examples=["battery_voltage"])]
    value: float
    unit: Annotated[str, Field(min_length=1, max_length=10, examples=["V"])]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Validateur Pydantic v2 : rejeter les données absurdes à la source
    @field_validator("value")
    @classmethod
    def validate_physical_thresholds(cls, v: float, info) -> float:
        metric = info.data.get("metric_name")
        # Exemple : la tension batterie ne peut pas être négative ni dépasser 36V
        if metric == "battery_voltage" and (v < 0.0 or v > 36.0):
            raise ValueError(f"Battery voltage out of physical range [0.0 - 36.0 V]: {v}")
        return v


class TelemetryPacketResponse(TelemetryPacketCreate):
    id: int
    severity: TelemetrySeverity
    received_at: datetime

    model_config = ConfigDict(from_attributes=True)