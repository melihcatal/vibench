import argparse
import os
from datetime import datetime, timedelta, timezone

import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", default=os.getenv("GOOGLE_CLOUD_PROJECT"))
    parser.add_argument("--api-key", default=os.getenv("GOOGLE_CLOUD_API_KEY"))
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--field", action="append", default=[])
    return parser.parse_args()


def build_filter(field_filters, start_time, end_time):
    clauses = [
        f'timestamp >= "{start_time.isoformat().replace("+00:00", "Z")}"',
        f'timestamp <= "{end_time.isoformat().replace("+00:00", "Z")}"',
    ]
    for item in field_filters:
        if "=" not in item:
            raise ValueError("--field must use key=value format")
        key, value = item.split("=", 1)
        clauses.append(f'jsonPayload.{key} = "{value}"')
    return " AND ".join(clauses)


def fetch_recent_logs(project_id, api_key, field_filters, hours, limit):
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT or --project-id is required")
    if not api_key:
        raise ValueError("GOOGLE_CLOUD_API_KEY or --api-key is required")

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    filter_expr = build_filter(field_filters, start_time, end_time)
    url = f"https://logging.googleapis.com/v2/projects/{project_id}/entries:list"
    payload = {
        "filter": filter_expr,
        "orderBy": "timestamp desc",
        "pageSize": limit,
    }
    response = requests.post(
        url,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json().get("entries", [])


def main():
    args = parse_args()
    entries = fetch_recent_logs(args.project_id, args.api_key, args.field, args.hours, args.limit)
    for entry in entries:
        timestamp = entry.get("timestamp", "")
        payload = entry.get("jsonPayload", entry.get("textPayload", entry))
        print(f"{timestamp} {payload}")


if __name__ == "__main__":
    main()
