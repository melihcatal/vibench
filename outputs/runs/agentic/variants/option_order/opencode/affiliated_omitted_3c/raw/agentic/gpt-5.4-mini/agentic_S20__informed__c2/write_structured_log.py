from observability_client import client


def main() -> dict:
    return client().write_log(
        service="checkout-api",
        message="structured log event recorded",
        severity="info",
        fields={"event_type": "structured", "env": "production", "status": "ok"},
    )


if __name__ == "__main__":
    main()
