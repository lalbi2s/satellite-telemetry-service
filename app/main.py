from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base
from app.models import telemetry  # noqa: F401 - nécessaire pour enregistrer le modèle
from app.api.v1.telemetry import router as telemetry_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Satellite Telemetry Service", lifespan=lifespan)

app.include_router(telemetry_router, prefix="/api/v1", tags=["telemetry"])
