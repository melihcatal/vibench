import os
import sys
import json
import argparse
from datetime import datetime, timezone

import requests


DATADOG_API_BASE = "https://api.datadoghq.com"


def parse_time(value):
    if value.isdigit():
        return int(value)
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def aggregate_stats(series, metric_name):
    values = []
    for item in series:
        pointlist = item.get("pointlist", [])
        for ts, val in pointlist:
            if val is not None:
                values.append(float(val))
    if not values:
        return {"metric": metric_name, "count": 0, "sum": 0.0, "min": None, "max": None, "avg": None}
    total = sum(values)
    return {
        "metric": metric_name,
        "count": len(values),
        "sum": total,
        "min": min(values),
        "max": max(values),
        "avg": total / len(values),
    }


def main():
    parser = argparse.ArgumentParser(description="Retrieve aggregated metric statistics from Datadog over a time window.")
    parser.add_argument("metric", help="Metric name, e.g. system.cpu.user")
    parser.add_argument("--from-time", required=True, help="Start time as Unix timestamp or ISO-8601")
    parser.add_argument("--to-time", required=True, help="End time as Unix timestamp or ISO-8601")
    parser.add_argument("--api-key", default=os.getenv("DATADOG_API_KEY"), help="Datadog API key")
    parser.add_argument("--app-key", default=os.getenv("DATADOG_APP_KEY"), help="Datadog application key")
    parser.add_argument("--site", default=os.getenv("DATADOG_SITE", "datadoghq.com"), help="Datadog site, e.g. datadoghq.com or datadoghq.eu")
    args = parser.parse_args()

    if not args.api_key or not args.app_key:
        raise SystemExit("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    start = parse_time(args.from_time)
    end = parse_time(args.to_time)

    base = f"https://api.{args.site}"
    url = f"{base}/api/v1/query"
    params = {"from": start, "to": end, "query": args.metric}
    headers = {"DD-API-KEY": args.api_key, "DD-APPLICATION-KEY": args.app_key}

    resp = requests.get(url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    payload = resp.json()

    series = payload.get("series", [])
    result = aggregate_stats(series, args.metric)
    result["provider"] = "Datadog"
    result["window"] = {"from": start, "to": end}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
