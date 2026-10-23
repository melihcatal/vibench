import time

from observability_client import query_recent_logs


def main() -> None:
    end_time = int(time.time())
    start_time = end_time - 900
    query_recent_logs(str(start_time), str(end_time), filters={"service": "checkout"}, limit=25)


if __name__ == "__main__":
    main()
