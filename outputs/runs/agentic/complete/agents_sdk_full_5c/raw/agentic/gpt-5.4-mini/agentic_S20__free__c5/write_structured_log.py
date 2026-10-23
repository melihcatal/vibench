from __future__ import annotations

from observability_client import build_openai_client, send_structured_log
from observability_models import LogEvent


def main() -> None:
    client = build_openai_client()
    event = LogEvent(
        message="Checkout completed successfully",
        severity="INFO",
        service="checkout-api",
        request_id="req-8b9f2c4e",
        fields={
            "order_id": "ord_10294",
            "amount_usd": 149.99,
            "region": "us-east-1",
        },
    )
    send_structured_log(client, event)


if __name__ == "__main__":
    main()
