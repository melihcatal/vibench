import argparse
import json
import os
from datetime import datetime, timezone

import requests


LOKI_API_URL = os.environ.get("LOKI_API_URL", "https://loki.example.com/loki/api/v1/query_range")
LOKI_API_TOKEN = os.environ.get("LOKI_API_TOKEN")


def parse_iso8601(value):
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def to_unix_ns(dt):
    return int(dt.astimezone(timezone.utc).timestamp() * 1_000_000_000)


def fetch_series(query, start_ns, end_ns, step_seconds):
    headers = {}
    if LOKI_API_TOKEN:
        headers["Authorization"] = f"Bearer {LOKI_API_TOKEN}"
    params = {
        "query": query,
        "start": str(start_ns),
        "end": str(end_ns),
        "step": str(step_seconds),
    }
    response = requests.get(LOKI_API_URL, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    result = payload.get("data", {}).get("result", [])
    series = []
    for item in result:
        values = item.get("values", [])
        for ts, val in values:
            series.append((int(ts), float(val)))
    series.sort(key=lambda x: x[0])
    return series


def summarize(series):
    if not series:
        return {"count": 0, "min": None, "max": None, "avg": None, "latest": None}
    values = [v for _, v in series]
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
        "latest": values[-1],
    }


def main():
    parser = argparse.ArgumentParser(description="Compare metric values for two resource or dimension filters over the same window using Grafana Loki.")
    parser.add_argument("--query-a", required=True)
    parser.add_argument("--query-b", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--step", type=int, default=60)
    args = parser.parse_args()

    start_dt = parse_iso8601(args.start)
    end_dt = parse_iso8601(args.end)
    start_ns = to_unix_ns(start_dt)
    end_ns = to_unix_ns(end_dt)

    series_a = fetch_series(args.query_a, start_ns, end_ns, args.step)
    series_b = fetch_series(args.query_b, start_ns, end_ns, args.step)

    output = {
        "provider": "Grafana Loki",
        "window": {"start": args.start, "end": args.end, "step_seconds": args.step},
        "a": {"query": args.query_a, "summary": summarize(series_a), "series": series_a},
        "b": {"query": args.query_b, "summary": summarize(series_b), "series": series_b},
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
