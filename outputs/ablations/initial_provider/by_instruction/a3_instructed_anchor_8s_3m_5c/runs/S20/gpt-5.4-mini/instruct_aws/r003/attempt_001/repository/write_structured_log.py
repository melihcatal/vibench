from observability_client import write_log_event


def main() -> None:
    write_log_event("structured log event", severity="INFO", request_id="req-1", service="checkout", action="write_structured_log")


if __name__ == "__main__":
    main()
