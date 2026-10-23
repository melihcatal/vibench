from datetime import datetime, timezone

from observability_client import get_logger
from observability_models import LogEvent


def write_structured_log(
    message: str, service: str = "checkout", severity: str = "INFO"
) -> dict:
    event = LogEvent(
        message=message,
        severity=severity,
        service=service,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    logger = get_logger()
    logger.log_struct(event.to_payload(), severity=severity)
    return event.to_payload()
