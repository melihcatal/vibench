import os
import uuid
from observability_client import datadog_api_base, datadog_headers, load_datadog_config, post_json, utc_now_iso
from observability_models import LogEvent


def main() -> dict:
    config = load_datadog_config()
    correlation_id = os.getenv("CORRELATION_ID", str(uuid.uuid4()))
    events = [
        LogEvent(message="request received", service=config.service, status="info", timestamp=utc_now_iso(), correlation_id=correlation_id, request_id="ingest-1"),
        LogEvent(message="downstream call completed", service=config.service, status="info", timestamp=utc_now_iso(), correlation_id=correlation_id, request_id="ingest-1"),
    ]
    payload = {"logs": [event.to_datadog_dict() for event in events]}
    return post_json(f"{datadog_api_base(config)}/api/v2/logs", datadog_headers(config), payload)


if __name__ == "__main__":
    print(main())
