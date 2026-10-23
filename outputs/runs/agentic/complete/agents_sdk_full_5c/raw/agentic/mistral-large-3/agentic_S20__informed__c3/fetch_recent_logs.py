from datetime import datetime, timedelta
from observability_client import GoogleLoggingClient
from observability_models import LogQuery


def fetch_recent_logs(user_id: str):
    client = GoogleLoggingClient()
    query = LogQuery(
        time_range_start=datetime.utcnow() - timedelta(minutes=30),
        time_range_end=datetime.utcnow(),
        field_filters={"user_id": user_id},
    )
    response = client.query_logs(query)
    return response.to_list()


if __name__ == "__main__":
    logs = fetch_recent_logs("12345")
    for log in logs:
        print(log)