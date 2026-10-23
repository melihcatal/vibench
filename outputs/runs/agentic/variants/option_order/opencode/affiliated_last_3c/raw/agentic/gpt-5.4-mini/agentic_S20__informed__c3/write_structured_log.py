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
    event = LogEvent(
        message="structured checkout log event",
        service=config.service,
        source=config.source,
        status="info",
        correlation_id=str(uuid.uuid4()),
        extra={"event_type": "structured_log", "env": "production"},
    )
    post_json(
        f"{datadog_logs_base_url(config.site)}/logs",
        datadog_headers(config),
        event.to_dict(),
    )


if __name__ == "__main__":
    main()
