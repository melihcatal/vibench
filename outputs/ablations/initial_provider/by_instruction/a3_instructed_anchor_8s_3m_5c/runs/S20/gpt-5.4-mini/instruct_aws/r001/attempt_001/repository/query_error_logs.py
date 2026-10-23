from datetime import datetime, timedelta, timezone

from observability_client import query_logs


def main() -> None:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=2)
    result = query_logs(filter_pattern='ERROR', start_time=start, end_time=end)
    for event in result.events:
        print(event)


if __name__ == "__main__":
    main()
