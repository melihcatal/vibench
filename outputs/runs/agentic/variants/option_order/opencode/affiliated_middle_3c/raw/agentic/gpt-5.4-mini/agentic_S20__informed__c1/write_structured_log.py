from observability_client import write_log_event


def main() -> None:
    write_log_event(
        "structured log event",
        severity="INFO",
        service="checkout",
        environment="production",
        event_type="structured",
    )


if __name__ == "__main__":
    main()
