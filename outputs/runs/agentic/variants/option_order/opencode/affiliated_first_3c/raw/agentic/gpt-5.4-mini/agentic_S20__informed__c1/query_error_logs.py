from observability_client import DatadogLogsClient
from observability_models import QueryWindow


def query_error_logs() -> dict:
    client = DatadogLogsClient.from_env()
    window = QueryWindow.recent_minutes(60)
    query = "service:api severity:error"
    return client.query_logs(
        query=query, start_time=window.start_time, end_time=window.end_time, limit=25
    )


if __name__ == "__main__":
    query_error_logs()
