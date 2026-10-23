from datetime import datetime, timedelta
from observability_client import GoogleCloudLoggingClient
from observability_models import LogQueryRequest


def query_error_logs(severities: list = None, hours: int = 1) -> list:
    client = GoogleCloudLoggingClient()
    query_request = LogQueryRequest(
        filter_severity=severities or ["ERROR", "CRITICAL"],
        time_from=datetime.utcnow() - timedelta(hours=hours),
        time_to=datetime.utcnow(),
        limit=100
    )
    response = client.query_logs(query_request)
    return response.entries


if __name__ == "__main__":
    errors = query_error_logs()
    for error in errors:
        print(error)