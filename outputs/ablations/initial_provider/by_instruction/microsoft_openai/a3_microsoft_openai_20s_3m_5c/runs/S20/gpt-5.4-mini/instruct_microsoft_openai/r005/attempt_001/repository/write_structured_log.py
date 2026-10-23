from observability_client import write_log
from observability_models import StructuredLogEvent


def main() -> dict:
    event = StructuredLogEvent(message="checkout completed", severity="info", service="billing", fields={"order_id": "ord_123", "amount": 42.5})
    return write_log(event)
