from observability_client import write_log_event


def main() -> None:
    request_id = "req-12345"
    write_log_event(
        "request started", severity="INFO", request_id=request_id, component="api"
    )
    write_log_event(
        "request completed",
        severity="INFO",
        request_id=request_id,
        component="api",
        duration_ms=84,
    )


if __name__ == "__main__":
    main()
