from observability_client import query_entries, recent_time_window
from observability_models import LogQuery


def main() -> list:
    window = recent_time_window(minutes=30)
    query = LogQuery(severity="ERROR", field_filters={"service": "ingestion"}, **window)
    return query_entries(query, log_name="structured-log")


if __name__ == "__main__":
    main()
