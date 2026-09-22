from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./telemetry.db"

    TEMP_THRESHOLD_MIN: float = -40.0
    TEMP_THRESHOLD_MAX: float = 85.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()