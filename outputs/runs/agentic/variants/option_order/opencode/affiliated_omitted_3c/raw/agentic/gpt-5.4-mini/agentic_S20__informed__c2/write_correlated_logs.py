from observability_client import client


def main() -> dict:
    correlation_id = "req-8f3c7a2d"
    logs = [
        ("checkout-api", "request received", "info"),
        ("checkout-worker", "payment authorization completed", "info"),
        ("checkout-api", "response sent", "info"),
    ]
    results = []
    c = client()
    for service, message, severity in logs:
        results.append(
            c.write_log(
                service=service,
                message=message,
                severity=severity,
                correlation_id=correlation_id,
                fields={"request_id": correlation_id},
            )
        )
    return {"correlation_id": correlation_id, "results": results}


if __name__ == "__main__":
    main()
