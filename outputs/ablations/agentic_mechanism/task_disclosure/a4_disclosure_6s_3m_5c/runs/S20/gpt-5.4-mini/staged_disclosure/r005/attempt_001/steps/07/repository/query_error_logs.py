import argparse
import os
from datetime import datetime, timezone

from google.cloud import logging_v2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--severity", default="ERROR")
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--project", default=os.getenv("GOOGLE_CLOUD_PROJECT"))
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.project:
        raise SystemExit("GOOGLE_CLOUD_PROJECT or --project is required")

    client = logging_v2.Client(project=args.project)
    end_time = datetime.now(timezone.utc)
    start_time = end_time.fromtimestamp(end_time.timestamp() - args.hours * 3600, tz=timezone.utc)
    filter_str = (
        f'severity>={args.severity} '
        f'AND timestamp>="{start_time.isoformat()}" '
        f'AND timestamp<="{end_time.isoformat()}"'
    )

    entries = client.list_entries(filter_=filter_str, order_by=logging_v2.DESCENDING)
    for entry in entries:
        ts = getattr(entry, "timestamp", None)
        payload = entry.payload
        print(f"{ts} {entry.severity} {payload}")


if __name__ == "__main__":
    main()
