import os
from observability_client import datadog_api_base, datadog_headers, load_datadog_config, post_json, utc_now_iso
from observability_models import LogEvent


def main() -> dict:
    config = load_datadog_config()
    event = LogEvent(
        message=os.getenv("LOG_MESSAGE", "structured application event"),
        service=config.service,
        status=os.getenv("LOG_STATUS", "info"),
        timestamp=utc_now_iso(),
        request_id=os.getenv("REQUEST_ID", "req-123"),
        attributes={"source": config.source, "env": os.getenv("DD_ENV", "dev")},
    )
    payload = {"logs": [event.to_datadog_dict()]}
    return post_json(f"{datadog_api_base(config)}/api/v2/logs", datadog_headers(config), payload)


if __name__ == "__main__":
    print(main())
