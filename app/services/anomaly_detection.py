from app.core.config import settings

TEMP_METRICS = {"temperature", "battery_temp"}


def detect_severity(metric_name: str, value: float) -> str:
    if metric_name in TEMP_METRICS:
        if value < settings.TEMP_THRESHOLD_MIN or value > settings.TEMP_THRESHOLD_MAX:
            return "CRITICAL"
        if value < settings.TEMP_THRESHOLD_MIN + 5 or value > settings.TEMP_THRESHOLD_MAX - 5:
            return "WARNING"
    return "NOMINAL"