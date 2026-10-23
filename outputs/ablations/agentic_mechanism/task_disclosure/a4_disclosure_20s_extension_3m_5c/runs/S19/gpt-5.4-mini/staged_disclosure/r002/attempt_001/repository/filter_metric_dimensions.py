import argparse
import json
import os
from datetime import datetime, timedelta, timezone

import requests


GRAFANA_CLOUD_API_BASE = "https://api.grafana.com"


def _parse_timestamp(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def _normalize_time(value: str | None) -> str:
    if value:
        return _parse_timestamp(value).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return (datetime.now(timezone.utc) - timedelta(minutes=15)).isoformat().replace("+00:00", "Z")


def query_metric_dimensions(org_id: str, query: str, start: str | None, end: str | None, step: str, filters: list[str]) -> dict:
    token = os.environ["GRAFANA_CLOUD_API_TOKEN"]
    url = f"{GRAFANA_CLOUD_API_BASE}/api/prometheus/{org_id}/api/v1/query_range"
    params = {"query": query, "start": _normalize_time(start), "end": _normalize_time(end), "step": step}
    if filters:
        params["query"] = f'{query}{{{",".join(filters)}}}' if "{" not in query else query
    response = requests.get(url, params=params, headers={"Authorization": f"Bearer {token}"}, timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> None:
    parser = argparse.ArgumentParser(description="Query Grafana Cloud metric data filtered by labels or dimensions.")
    parser.add_argument("--org-id", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--step", default="60s")
    parser.add_argument("--filter", action="append", default=[])
    args = parser.parse_args()
    print(json.dumps(query_metric_dimensions(args.org_id, args.query, args.start, args.end, args.step, args.filter), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
