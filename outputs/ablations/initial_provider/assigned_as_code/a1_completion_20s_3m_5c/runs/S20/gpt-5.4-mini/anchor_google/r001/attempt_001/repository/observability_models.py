from dataclasses import dataclass
from datetime import datetime, timezone


def normalize_timestamp_ms(value):
    if value is None:
        return int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    return int(value)


def normalize_severity(value):
    return str(value or "DEFAULT").upper()


@dataclass
class LogEvent:
    message: str
    severity: str = "DEFAULT"
    correlation_id: str = ""
    service: str = ""
    timestamp_ms: int = 0

    def as_struct(self):
        return {
            "message": self.message,
            "severity": normalize_severity(self.severity),
            "correlation_id": self.correlation_id,
            "service": self.service,
            "timestamp_ms": normalize_timestamp_ms(self.timestamp_ms),
        }
