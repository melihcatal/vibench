from datetime import datetime, timedelta
from observability_client import GoogleCloudLoggingClient
from observability_models import LogQueryRequest


def fetch_recent_logs(correlation_id: str = None, hours: int = 1) -> list:
    client = GoogleCloudLoggingClient()
    query_request = LogQueryRequest(
        correlation_id=correlation_id,
        time_from=datetime.utcnow() - timedelta(hours=hours),
        time_to=datetime.utcnow(),
        limit=50
    )
    response = client.query_logs(query_request)
    return response.entries


if __name__ == "__main__":
    logs = fetch_recent_logs(correlation_id="req-12345")
    for log in logs:
        print(log)