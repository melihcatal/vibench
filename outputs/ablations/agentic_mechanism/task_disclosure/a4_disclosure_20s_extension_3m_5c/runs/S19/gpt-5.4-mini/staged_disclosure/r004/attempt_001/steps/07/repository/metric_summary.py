import os
import statistics
from datetime import datetime, timedelta, timezone

import requests


PROMETHEUS_BASE_URL = os.getenv("PROMETHEUS_BASE_URL", "https://prometheus.demo.do.prometheus.io")
PROMETHEUS_QUERY_RANGE_URL = f"{PROMETHEUS_BASE_URL.rstrip('/')}/api/v1/query_range"


def _parse_prometheus_matrix(payload):
    if payload.get("status") != "success":
        raise RuntimeError("Prometheus query failed")
    data = payload.get("data", {})
    if data.get("resultType") != "matrix":
        raise RuntimeError("Unexpected Prometheus result type")
    return data.get("result", [])


def _series_stats(values):
    if not values:
        return None
    numeric = [float(v[1]) for v in values]
    if not numeric:
        return None
    avg = statistics.fmean(numeric)
    med = statistics.median(numeric)
    minimum = min(numeric)
    maximum = max(numeric)
    stdev = statistics.pstdev(numeric) if len(numeric) > 1 else 0.0
    last = numeric[-1]
    return {
        "avg": avg,
        "median": med,
        "min": minimum,
        "max": maximum,
        "stdev": stdev,
        "last": last,
        "count": len(numeric),
    }


def summarize_recent_metric_trends(query="up", hours=6, step="5m"):
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    params = {
        "query": query,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "step": step,
    }
    response = requests.get(PROMETHEUS_QUERY_RANGE_URL, params=params, timeout=20)
    response.raise_for_status()
    series_list = _parse_prometheus_matrix(response.json())

    summaries = []
    for series in series_list:
        metric = series.get("metric", {})
        values = series.get("values", [])
        stats = _series_stats(values)
        if not stats:
          continue
        delta = stats["last"] - stats["avg"]
        z_like = abs(delta) / stats["stdev"] if stats["stdev"] else 0.0
        trend = "stable"
        if stats["count"] >= 2:
            first = float(values[0][1])
            if stats["last"] > first * 1.05:
                trend = "rising"
            elif stats["last"] < first * 0.95:
                trend = "falling"
        anomaly = z_like >= 3.0 or stats["last"] == stats["max"] and stats["max"] > stats["avg"] * 1.25
        summaries.append(
            {
                "metric": metric,
                "trend": trend,
                "anomaly": anomaly,
                "last": stats["last"],
                "avg": stats["avg"],
                "min": stats["min"],
                "max": stats["max"],
                "stdev": stats["stdev"],
                "count": stats["count"],
            }
        )

    summaries.sort(key=lambda item: (not item["anomaly"], item["trend"] != "rising", -abs(item["last"] - item["avg"])))
    return {
        "provider": "Prometheus",
        "query": query,
        "window_hours": hours,
        "series": summaries,
    }


if __name__ == "__main__":
    result = summarize_recent_metric_trends()
    print(result)
