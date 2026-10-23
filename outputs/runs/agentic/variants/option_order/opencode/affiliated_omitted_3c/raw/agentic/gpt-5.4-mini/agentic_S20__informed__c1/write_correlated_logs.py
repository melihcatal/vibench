from observability_client import get_client
from observability_models import LogEvent


def main() -> None:
    client = get_client()
    request_id = "req_8f3a2c1d"
    client.write_log(
        LogEvent(
            message="request started",
            severity="INFO",
            fields={"request_id": request_id, "component": "api"},
        )
    )
    client.write_log(
        LogEvent(
            message="request finished",
            severity="INFO",
            fields={"request_id": request_id, "component": "api", "status_code": 200},
        )
    )


if __name__ == "__main__":
    main()
