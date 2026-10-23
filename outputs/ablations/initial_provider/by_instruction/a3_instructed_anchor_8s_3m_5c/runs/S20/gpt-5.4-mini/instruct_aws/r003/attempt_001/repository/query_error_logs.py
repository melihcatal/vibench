import time

from observability_client import query_recent_logs


def main() -> None:
    end_time = int(time.time())
    start_time = end_time - 3600
    query_recent_logs(str(start_time), str(end_time), filters={"severity": "ERROR"}, limit=50)


if __name__ == "__main__":
    main()
