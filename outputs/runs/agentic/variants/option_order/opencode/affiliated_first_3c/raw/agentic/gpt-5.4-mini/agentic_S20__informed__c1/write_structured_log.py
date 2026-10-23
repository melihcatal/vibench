from observability_client import DatadogLogsClient, build_log_event


def write_structured_log() -> dict:
    client = DatadogLogsClient.from_env()
    event = build_log_event(
        "structured checkout event",
        severity="INFO",
        fields={
            "service": "checkout",
            "environment": "production",
            "order_id": "ord_1001",
            "event_type": "purchase_completed",
        },
    )
    return client.write_event(event)


if __name__ == "__main__":
    write_structured_log()
