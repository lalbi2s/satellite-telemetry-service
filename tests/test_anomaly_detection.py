from app.services.anomaly_detection import detect_severity


def test_nominal_temperature():
    assert detect_severity("temperature", 20.0) == "NOMINAL"


def test_warning_temperature_high():
    assert detect_severity("temperature", 82.0) == "WARNING"


def test_warning_temperature_low():
    assert detect_severity("temperature", -38.0) == "WARNING"


def test_critical_temperature_too_high():
    assert detect_severity("temperature", 95.0) == "CRITICAL"


def test_critical_temperature_too_low():
    assert detect_severity("temperature", -50.0) == "CRITICAL"


def test_non_temperature_metric_is_nominal():
    assert detect_severity("battery_voltage", 1000.0) == "NOMINAL"