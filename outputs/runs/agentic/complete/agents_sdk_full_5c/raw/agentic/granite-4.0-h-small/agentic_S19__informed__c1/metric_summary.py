# LATER-STEP: metric_summary.py
from datetime import datetime, timedelta
from observability_client import MetricsClient
from observability_models import MetricQueryRequest, MetricWindow

SUMMARIZER = {
    "provider": "datadog",
    "model": "gpt-4o-mini",
}

def metric_summary(metric: str, lookback: timedelta = timedelta(days=7)) -> str:
    end = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    start = (datetime.utcnow() - lookback).strftime("%Y-%m-%dT%H:%M:%SZ")
    request = MetricQueryRequest(metric=metric, window=MetricWindow(start=start, end=end), limit=100)
    raw = MetricsClient.get().query(request)
    # Very simple summarization logic based on last point
    points = raw.get('downtime', {}).get('series', [])
    if points:
        latest = points[-1][1]
        trend = 'increasing' if latest > 0.5 else 'stable'
    else:
        trend = 'no data'
    return f"Metric {metric} over the last {lookback} shows a {trend} trend."

if __name__ == "__main__":
    # Example with Datadog (set DD_API_KEY, DD_APP_KEY)
    print(metric_summary("system.cpu.idle"))
