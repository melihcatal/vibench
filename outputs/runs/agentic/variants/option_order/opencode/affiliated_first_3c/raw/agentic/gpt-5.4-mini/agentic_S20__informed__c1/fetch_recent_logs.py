from observability_client import DatadogLogsClient
from observability_models import QueryWindow


def fetch_recent_logs() -> dict:
    client = DatadogLogsClient.from_env()
    window = QueryWindow.recent_minutes(15)
    query = "service:checkout environment:production"
    return client.query_logs(
        query=query, start_time=window.start_time, end_time=window.end_time, limit=50
    )


if __name__ == "__main__":
    fetch_recent_logs()
