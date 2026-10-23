from observability_client import GoogleLoggingClient
from observability_models import LogQuery
from datetime import datetime, timedelta
import argparse


def query_error_logs(severity: str = "ERROR", hours: int = 1) -> None:
    client = GoogleLoggingClient()
    time_from = datetime.utcnow() - timedelta(hours=hours)
    log_query = LogQuery(
        filter_severity=severity,
        time_from=time_from,
        custom_filters={"source": "application"},
    )
    response = client.query_logs(log_query)
    for entry in response.entries:
        print(f"{entry['timestamp']} [{entry['severity']}] {entry['message']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--severity", type=str, default="ERROR")
    parser.add_argument("--hours", type=int, default=1)
    args = parser.parse_args()
    query_error_logs(args.severity, args.hours)