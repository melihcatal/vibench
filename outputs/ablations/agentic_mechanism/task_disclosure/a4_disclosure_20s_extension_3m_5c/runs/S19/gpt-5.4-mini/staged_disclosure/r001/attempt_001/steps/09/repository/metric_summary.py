import json
import os
import statistics
from datetime import datetime, timedelta, timezone
from typing import Any

import requests


def _parse_timestamp(value: Any) -> datetime:
    if isinstance(value, (int, float)):
        if value > 10_000_000_000:
            value /= 1000.0
        return datetime.fromtimestamp(value, tz=timezone.utc)
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            pass
    raise ValueError("Unsupported timestamp format")


def _fetch_datadog_metrics() -> list[dict[str, Any]]:
    site = os.getenv("DATADOG_SITE", "datadoghq.com")
    api_key = os.getenv("DATADOG_API_KEY")
    app_key = os.getenv("DATADOG_APP_KEY")
    query = os.getenv("DATADOG_METRIC_QUERY", "avg:system.cpu.user{*}")
    if not api_key or not app_key:
        raise RuntimeError("DATADOG_API_KEY and DATADOG_APP_KEY are required")
    end = int(datetime.now(tz=timezone.utc).timestamp())
    start = int((datetime.now(tz=timezone.utc) - timedelta(days=7)).timestamp())
    url = f"https://api.{site}/api/v1/query"
    response = requests.get(
        url,
        params={"from": start, "to": end, "query": query},
        headers={"DD-API-KEY": api_key, "DD-APPLICATION-KEY": app_key},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    series = payload.get("series", [])
    if not series:
        return []
    points = series[0].get("pointlist", [])
    return [{"timestamp": ts, "value": val} for ts, val in points if val is not None]


def _summarize(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"count": 0, "trend": "no data", "anomalies": []}
    count = len(values)
    first_window = values[: max(1, count // 4)]
    last_window = values[-max(1, count // 4):]
    first_avg = statistics.fmean(first_window)
    last_avg = statistics.fmean(last_window)
    overall_avg = statistics.fmean(values)
    stdev = statistics.pstdev(values) if count > 1 else 0.0
    trend_delta = ((last_avg - first_avg) / first_avg * 100.0) if first_avg else 0.0
    anomalies = []
    threshold = overall_avg + (2.5 * stdev)
    for idx, value in enumerate(values):
        if value > threshold and stdev > 0:
            anomalies.append({"index": idx, "value": value})
    direction = "upward" if trend_delta > 5 else "downward" if trend_delta < -5 else "flat"
    return {
        "count": count,
        "overall_average": overall_avg,
        "trend": direction,
        "trend_change_percent": trend_delta,
        "anomalies": anomalies[:10],
    }


def main() -> None:
    data = _fetch_datadog_metrics()
    values = [float(item["value"]) for item in data if item.get("value") is not None]
    summary = _summarize(values)
    print(json.dumps(summary, separators=(",", ":"), sort_keys=True))


if __name__ == "__main__":
    main()
