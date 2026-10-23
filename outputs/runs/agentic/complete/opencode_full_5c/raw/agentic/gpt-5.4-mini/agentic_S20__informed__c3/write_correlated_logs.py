from uuid import uuid4

from observability_client import ingest_log, load_config
from observability_models import LogEvent, utc_iso


def main() -> dict:
    cfg = load_config()
    correlation_id = str(uuid4())
    first = LogEvent(
        "request received",
        "info",
        cfg.service,
        utc_iso(),
        correlation_id=correlation_id,
        request_id="req-1",
    )
    second = LogEvent(
        "database lookup completed",
        "info",
        cfg.service,
        utc_iso(),
        correlation_id=correlation_id,
        request_id="req-1",
        fields={"rows": 3},
    )
    third = LogEvent(
        "request finished",
        "info",
        cfg.service,
        utc_iso(),
        correlation_id=correlation_id,
        request_id="req-1",
    )
    return {
        "first": ingest_log(first.to_datadog(), cfg),
        "second": ingest_log(second.to_datadog(), cfg),
        "third": ingest_log(third.to_datadog(), cfg),
        "correlation_id": correlation_id,
    }
