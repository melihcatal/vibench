from observability_client import put_log_event


def main() -> None:
    put_log_event("structured log event", level="INFO", service="checkout", env="prod", aws_provider="cloudwatch-logs")


if __name__ == "__main__":
    main()
