from observability_client import GoogleLoggingClient
from observability_models import LogQuery
from datetime import datetime, timedelta
import argparse


def fetch_recent_logs(component: str, hours: int = 1) -> None:
    client = GoogleLoggingClient()
    time_from = datetime.utcnow() - timedelta(hours=hours)
    log_query = LogQuery(
        time_from=time_from,
        custom_filters={"component": component, "source": "application"},
    )
    response = client.query_logs(log_query)
    for entry in response.entries:
        print(f"{entry['timestamp']} [{entry['severity']}] {entry['message']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--component", type=str, required=True)
    parser.add_argument("--hours", type=int, default=1)
    args = parser.parse_args()
    fetch_recent_logs(args.component, args.hours)