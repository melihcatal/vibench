import argparse
import os
from datetime import datetime, timezone

import requests


LOKI_QUERY_RANGE_URL = "https://logs-prod-us.grafana.net/loki/api/v1/query_range"


def parse_time(value):
    if value is None:
        return None
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def to_ns(dt):
    return int(dt.timestamp() * 1_000_000_000)


def build_query(severity):
    return f'{{severity="{severity}"}}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--severity", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    username = os.environ.get("GRAFANA_CLOUD_LOGS_USERNAME")
    token = os.environ.get("GRAFANA_CLOUD_API_KEY")
    if not username or not token:
        raise SystemExit("GRAFANA_CLOUD_LOGS_USERNAME and GRAFANA_CLOUD_API_KEY are required")

    start_dt = parse_time(args.start)
    end_dt = parse_time(args.end)
    params = {
        "query": build_query(args.severity),
        "start": to_ns(start_dt),
        "end": to_ns(end_dt),
        "limit": args.limit,
    }

    response = requests.get(
        LOKI_QUERY_RANGE_URL,
        params=params,
        auth=(username, token),
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    for stream in data.get("data", {}).get("result", []):
        labels = stream.get("stream", {})
        for ts, line in stream.get("values", []):
            print(f"{ts} {labels} {line}")


if __name__ == "__main__":
    main()
