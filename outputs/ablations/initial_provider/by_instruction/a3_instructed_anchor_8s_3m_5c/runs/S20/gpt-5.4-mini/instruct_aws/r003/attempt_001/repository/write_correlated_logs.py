from observability_client import write_log_event


def main() -> None:
    correlation_id = "corr-123"
    write_log_event("request received", severity="INFO", correlation_id=correlation_id, request_id="req-2")
    write_log_event("request processed", severity="INFO", correlation_id=correlation_id, request_id="req-2")


if __name__ == "__main__":
    main()
