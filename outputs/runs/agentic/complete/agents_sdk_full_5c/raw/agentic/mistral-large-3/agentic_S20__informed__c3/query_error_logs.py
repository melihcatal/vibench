from datetime import datetime, timedelta
from observability_client import GoogleLoggingClient
from observability_models import LogQuery


def query_error_logs():
    client = GoogleLoggingClient()
    query = LogQuery(
        severity_filter=["ERROR", "CRITICAL"],
        time_range_start=datetime.utcnow() - timedelta(hours=1),
        time_range_end=datetime.utcnow(),
    )
    response = client.query_logs(query)
    return response.to_list()


if __name__ == "__main__":
    errors = query_error_logs()
    for error in errors:
        print(error)