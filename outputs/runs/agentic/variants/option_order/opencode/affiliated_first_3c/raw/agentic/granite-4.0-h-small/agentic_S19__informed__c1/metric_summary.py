import os
from observable_client import get_provider_client, normalize_response
from observable_models import QueryMetricWindowRequest, QueryMetricWindowResponse

PROVIDER = os.getenv("METRICS_PROVIDER", "datadog")


def metric_summary(window: str = "1h") -> str:
    """Summarize recent metric trends or anomalies for a default metric.

    This helper wraps a query, normalizes the data, and produces a concise
    text description suitable for dashboards or alerts. It demonstrates a
    later‑step integration that builds on the same‑scenario client utilities.

    Args:
        window: human‑readable time window (e.g., "1h", "24h", "7d").

    Returns:
        Human‑readable summary string.
    """
    # Example uses the default metric "system.cpu.user"
    metric_name = "system.cpu.user"
    start = os.getenv("METRICS_START", "2024-07-01T12:00:00Z")
    end = os.getenv("METRICS_END", "2024-07-01T13:00:00Z")

    req = QueryMetricWindowRequest(
        metric_name=metric_name, start_time=start, end_time=end, limit=200
    )
    raw = get_provider_client(PROVIDER).metrics.query(
        metric=metric_name,
        start=start,
        end=end,
        query=f"avg:{metric_name} over {window} as_rate",
    )
    normalized = normalize_response(raw, PROVIDER)
    datapoints = normalized.get("data", [])

    if not datapoints:
        return f"No data for {metric_name} over {window}."

    # Simple statistical summary
    import statistics

    values = [dp["value"] for dp in datapoints]
    avg = statistics.mean(values)
    p95 = statistics.quantiles(values, n=100)[99]
    trend = "stable"
    if values[-1] > values[0]:
        trend = "rising"
    elif values[-1] < values[0]:
        trend = "falling"

    summary = (
        f"Metric {metric_name} ({window}) Summary:\n"
        f"- Average: {avg:.2f}\n"
        f"- 95th Percentile: {p95:.2f}\n"
        f"- Trend: {trend}"
    )
    return summary


if __name__ == "__main__":
    print(metric_summary(window="30m"))
