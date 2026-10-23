from observability_client import ingest_log, load_config
from observability_models import LogEvent, utc_iso


def main() -> dict:
    cfg = load_config()
    event = LogEvent(
        message="structured checkout completed",
        level="info",
        service=cfg.service,
        timestamp=utc_iso(),
        fields={
            "event_type": "checkout",
            "order_id": "ord_12345",
            "amount": 49.95,
            "currency": "USD",
        },
    )
    return ingest_log(event.to_datadog(), cfg)
