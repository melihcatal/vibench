import os
from datetime import datetime, timedelta
from observability_client import get_cloudwatch_client
from observability_models import MetricQueryRequest

def summarize_recent_trends(metric_name, namespace, dimension_filters=None):
    """Summarize recent metric trends or anomalies using Amazon CloudWatch Metrics.

    Args:
        metric_name (str): Name of the CloudWatch metric.
        namespace (str): Namespace that contains the metric.
        dimension_filters (list): Optional list of dimension dicts to filter by.

    Returns:
        dict: High-level summary including latest value, min, max, and anomaly flag.
    """
    client = get_cloudwatch_client()
    now = datetime.utcnow()
    end = now.isoformat() + "Z"
    start = (now - timedelta(minutes=30)).isoformat() + "Z"
    period = 60  # 1‑minute granularity

    req = MetricQueryRequest(namespace, metric_name, start, end, period)
    if dimension_filters:
        req.dimensions = dimension_filters
    resp_raw = client.get_metric_statistics(**req.to_boto_params())
    datapoints = resp_raw.get("Datapoints", [])
    if not datapoints:
        return {"error": "No data points found"}
    # Convert to Python datetime objects for ease of analysis
    for dp in datapoints:
        dp["Timestamp"] = datetime.fromisoformat(dp["Timestamp"].replace("Z", "+00:00"))
        dp["Value"] = float(dp["Value"])
    # Simple summary: earliest, latest, min, max, average
    sorted_pts = sorted(datapoints, key=lambda dp: dp["Timestamp"])
    summary = {
        "earliest_timestamp": sorted_pts[0]["Timestamp"],
        "latest_timestamp": sorted_pts[-1]["Timestamp"],
        "min_value": min(p["Value"] for p in datapoints),
        "max_value": max(p["Value"] for p in datapoints),
        "average_value": sum(p["Value"] for p in datapoints) / len(datapoints),
    }
    # Basic anomaly heuristic: >2σ from mean -> flag
    mean = summary["average_value"]
    stdev = (sum((p["Value"] - mean) ** 2 for p in datapoints) / len(datapoints)) ** 0.5
    flagged = any(abs(p["Value"] - mean) > 2 * stdev for p in datapoints)
    summary["anomaly_detected"] = flagged
    return summary

if __name__ == "__main__":
    # Example: summarize CPUUtilization for a specific EC2 instance over the last 30 min.
    instance_id = os.getenv("AWS_INSTANCE_ID")
    dims = [{"Name": "InstanceId", "Value": instance_id}] if instance_id else None
    summary = summarize_recent_trends(
        os.getenv("AWS_METRIC_NAME", "CPUUtilization"),
        os.getenv("AWS_NAMESPACE", "AWS/EC2"),
        dimension_filters=dims,
    )
    print(summary)
