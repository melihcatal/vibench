# metric_summary.py
# LATER-STEP: Summarize recent metric trends or anomalies

from observability_client import ObservabilityClient
from observability_models import MetricSummaryRequest, MetricSummaryResponse


def summarize_recent_metrics(
    metric: str, start_time: str = None, end_time: str = None, window: str = "P1H"
) -> str:
    """Produce a concise textual summary of recent metric behavior.

    The function queries raw datapoints, computes simple statistics, and returns
    a human‑readable summary.  In production you would replace the static logic
    with provider‑specific anomaly detection models or custom thresholds.

    Args:
        metric: Metric name (e.g., "cpu.usage").
        start_time: ISO‑8601 start timestamp (optional).
        end_time: ISO‑8601 end timestamp (optional).
        window: Relative window (e.g., "P1H").

    Returns:
        A short summary string (max a few sentences).
    """
    client = ObservabilityClient()

    # Fetch raw datapoints using the generic query wrapper
    query_resp = query_metric_window(metric, start_time, end_time, window)
    values = query_resp.get_values()

    if not values:
        return "No data available for the requested metric/window."

    avg = sum(values) / len(values)
    min_val, max_val = min(values), max(values)
    # Simple anomaly heuristic: >2× average is flagged
    anomaly = any(v > 2 * avg for v in values)

    summary = (
        f"Metric {metric} over the last {window} shows an average of {avg:.2f}. "
        f"Minimum {min_val} and maximum {max_val}. "
    )
    if anomaly:
        summary += "⚠ Anomaly detected: some points exceed twice the average."
    else:
        summary += "No significant anomalies detected."
    return summary


# Example CLI usage for local testing
if __name__ == "__main__":
    print(summarize_recent_metrics("memory.usage", window="P2H"))
