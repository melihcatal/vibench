# [LATER-STEP] metric_summary.py
import observability_client as client
import observability_models as models


def summarize_recent_trends(metric_name: str, start_time: str, end_time: str):
    """Summarize recent metric trends or anomalies based on queried data.
    Uses the concrete provider (e.g., Datadog) via the helper client.
    """
    raw = client.query(metric=metric_name, start=start_time, end=end_time)
    normalized = models.normalize_response(raw)
    # Simple heuristic: look for increasing or decreasing series
    if not normalized["series"]:
        return {"summary": "No data available"}
    # Placeholder logic - compute simple trend direction from last two points
    points = [d["value"] for d in normalized["series"] if "value" in d]
    if len(points) < 2:
        trend = "Insufficient data"
    elif points[-1] > points[-2]:
        trend = "Increasing"
    else:
        trend = "Decreasing"
    return {"summary": f"Recent trend for {metric_name}: {trend}"}
