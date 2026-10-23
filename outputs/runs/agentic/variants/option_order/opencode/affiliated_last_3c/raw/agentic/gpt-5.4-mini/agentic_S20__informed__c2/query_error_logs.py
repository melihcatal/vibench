from observability_client import default_time_range, query_logs
from observability_models import LogQuery


def main() -> list[dict]:
    start, end = default_time_range(60)
    query = LogQuery(start_time=start, end_time=end, severity="ERROR")
    return query_logs(query)


if __name__ == "__main__":
    main()
