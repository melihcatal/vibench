import argparse
import os
from datetime import datetime, timezone

from google.cloud import logging_v2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--severity", default="ERROR")
    parser.add_argument("--minutes", type=int, default=60)
    parser.add_argument("--project", default=os.getenv("GOOGLE_CLOUD_PROJECT"))
    return parser.parse_args()


def main():
    args = parse_args()
    client = logging_v2.Client(project=args.project)
    end = datetime.now(timezone.utc)
    start = end.timestamp() - args.minutes * 60
    start_time = datetime.fromtimestamp(start, tz=timezone.utc).isoformat()
    end_time = end.isoformat()
    filt = (
        f'severity>={args.severity} '
        f'AND timestamp>="{start_time}" '
        f'AND timestamp<="{end_time}"'
    )
    entries = client.list_entries(filter_=filt, order_by=logging_v2.DESCENDING)
    for entry in entries:
        payload = entry.payload
        print(f"{entry.timestamp} {entry.severity} {payload}")


if __name__ == "__main__":
    main()
