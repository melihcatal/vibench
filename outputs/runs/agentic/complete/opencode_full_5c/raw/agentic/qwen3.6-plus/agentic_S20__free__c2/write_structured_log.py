from datetime import datetime, timezone

from observability_models import LogEvent, LogWriteResponse
from observability_client import send_log_events


def write_structured_log(
    message: str,
    status: str = "info",
    service: str = "",
    source: str = "python",
    tags: list[str] | None = None,
    attributes: dict | None = None,
) -> LogWriteResponse:
    event = LogEvent(
        message=message,
        status=status,
        service=service,
        source=source,
        tags=tags or [],
        timestamp=datetime.now(timezone.utc),
        attributes=attributes or {},
    )
    return send_log_events([event])


if __name__ == "__main__":
    result = write_structured_log(
        message="User login successful",
        status="info",
        service="auth-service",
        source="python",
        tags=["env:production", "team:identity"],
        attributes={
            "user_id": "usr_abc123",
            "login_method": "oauth2",
            "ip_address": "192.168.1.100",
        },
    )
    print(result)
