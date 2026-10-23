from datetime import datetime, timezone

from observability_client import get_logger
from observability_models import LogEvent


def write_correlated_logs(
    request_id: str, messages: list[str], service: str = "api"
) -> list[dict]:
    logger = get_logger()
    events = []
    for message in messages:
        event = LogEvent(
            message=message,
            request_id=request_id,
            correlation_id=request_id,
            service=service,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        payload = event.to_payload()
        logger.log_struct(payload, severity=payload.get("severity", "INFO"))
        events.append(payload)
    return events
