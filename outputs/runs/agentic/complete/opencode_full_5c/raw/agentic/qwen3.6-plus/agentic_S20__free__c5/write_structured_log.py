import json
from observability_models import LogEvent, LogLevel, now_iso
from observability_client import ingest_log_event


def write_structured_log(
    message: str,
    level: LogLevel = LogLevel.INFO,
    service: str = "web-api",
    source: str = "python",
    hostname: str = "",
    tags: list[str] | None = None,
    attributes: dict | None = None,
) -> dict:
    event = LogEvent(
        message=message,
        level=level,
        service=service,
        source=source,
        hostname=hostname,
        tags=tags or [],
        attributes=attributes or {},
        timestamp=now_iso(),
    )
    result = ingest_log_event(event)
    return result


if __name__ == "__main__":
    result = write_structured_log(
        message="User login successful",
        level=LogLevel.INFO,
        service="auth-service",
        source="python",
        tags=["env:production", "team:identity"],
        attributes={"user_id": "usr_42", "method": "oauth2"},
    )
    print(json.dumps(result, indent=2))
