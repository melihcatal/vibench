from observability_client import put_log_event


def main() -> None:
    request_id = "req-12345"
    put_log_event("request started", level="INFO", request_id=request_id, service="api", aws_provider="cloudwatch-logs")
    put_log_event("request completed", level="INFO", request_id=request_id, service="api", status="ok", aws_provider="cloudwatch-logs")


if __name__ == "__main__":
    main()
