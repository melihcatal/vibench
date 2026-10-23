import os
from datetime import datetime, timedelta, timezone

import requests


def _fetch_prometheus_range(query, start, end, step):
    base_url = os.environ.get("PROMETHEUS_URL", "https://prometheus.io/api/v1")
    token = os.environ.get("PROMETHEUS_BEARER_TOKEN")
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(
        f"{base_url.rstrip('/')}/query_range",
        params={
            "query": query,
            "start": start.isoformat(),
            "end": end.isoformat(),
            "step": step,
        },
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "success":
        raise RuntimeError(payload)
    return payload.get("data", {}).get("result", [])


def _parse_series(result):
    values = []
    for series in result:
        for ts, value in series.get("values", []):
            try:
                values.append((float(ts), float(value)))
            except (TypeError, ValueError):
                continue
    return values


def _summarize(values):
    if not values:
        return "No metric data returned."
    points = [v for _, v in values]
    first, last = points[0], points[-1]
    minimum = min(points)
    maximum = max(points)
    mean = sum(points) / len(points)
    delta = last - first
    pct = (delta / first * 100.0) if first not in (0, 0.0) else None
    sorted_points = sorted(points)
    p95 = sorted_points[int(max(0, round(0.95 * (len(sorted_points) - 1))))]
    anomalies = [v for v in points if v > mean + 2 * ((sum((x - mean) ** 2 for x in points) / len(points)) ** 0.5)]
    parts = [
        f"points={len(points)}",
        f"start={first:.4f}",
        f"end={last:.4f}",
        f"min={minimum:.4f}",
        f"max={maximum:.4f}",
        f"mean={mean:.4f}",
        f"p95={p95:.4f}",
        f"trend={'up' if delta > 0 else 'down' if delta < 0 else 'flat'}",
    ]
    if pct is not None:
        parts.append(f"change={pct:.2f}%")
    if anomalies:
        parts.append(f"high_anomalies={len(anomalies)}")
    return "; ".join(parts)


def main():
    query = os.environ.get("PROMETHEUS_QUERY", "up")
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=int(os.environ.get("METRIC_LOOKBACK_HOURS", "24")))
    step = os.environ.get("PROMETHEUS_STEP", "5m")
    result = _fetch_prometheus_range(query, start, end, step)
    values = _parse_series(result)
    print(_summarize(values))


if __name__ == "__main__":
    main()
