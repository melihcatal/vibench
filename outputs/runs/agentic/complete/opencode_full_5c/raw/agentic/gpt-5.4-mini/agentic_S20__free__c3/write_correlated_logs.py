from observability_client import default_client
from observability_models import LogEvent


def main() -> list:
    client = default_client()
    request_id = "req-abc-123"
    return [
        client.write_event(
            LogEvent(
                message="request.started",
                severity="INFO",
                service="api",
                request_id=request_id,
                correlation_id=request_id,
            )
        ),
        client.write_event(
            LogEvent(
                message="request.completed",
                severity="INFO",
                service="api",
                request_id=request_id,
                correlation_id=request_id,
                fields={"status_code": 200},
            )
        ),
    ]


if __name__ == "__main__":
    main()
