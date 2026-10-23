import uuid

from observability_client import (
    datadog_headers,
    datadog_logs_base_url,
    load_config,
    post_json,
)
from observability_models import LogEvent


def main() -> None:
    config = load_config()
    request_id = str(uuid.uuid4())
    shared = str(uuid.uuid4())
    for status, message in (
        ("info", "request received"),
        ("info", "request processed"),
        ("error", "request completed with warning"),
    ):
        event = LogEvent(
            message=message,
            service=config.service,
            source=config.source,
            status=status,
            request_id=request_id,
            correlation_id=shared,
            extra={"span_id": str(uuid.uuid4())},
        )
        post_json(
            f"{datadog_logs_base_url(config.site)}/logs",
            datadog_headers(config),
            event.to_dict(),
        )


if __name__ == "__main__":
    main()
