import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import anthropic
from observability_client import ObservabilityClient
from observability_models import MetricStatistics, ResponseNormalizer, TimeWindow
import pytz


def summarize_metric_trends(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimension_filters: Optional[Dict[str, str]] = None,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Summarize recent metric trends or anomalies using Anthropic Claude.

    Args:
        metric_name: The metric type name
        start_time: Start of the time window
        end_time: End of the time window
        dimension_filters: Optional dimension filters
        project_id: Google Cloud project ID

    Returns:
        Summary with trend analysis and anomaly detection
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

    client = ObservabilityClient(project_id)

    time_series_list = client.query_time_series(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimension_filters=dimension_filters,
        alignment_period_seconds=300,
    )

    if not time_series_list:
        return {
            "metric_name": metric_name,
            "time_window": TimeWindow(start_time, end_time).to_dict(),
            "summary": "No data available for the specified metric and time window.",
            "has_data": False,
            "anomalies": [],
            "trend": "unknown",
        }

    normalized_series = [
        ResponseNormalizer.normalize_time_series(ts) for ts in time_series_list
    ]

    stats = ResponseNormalizer.normalize_statistics(
        metric_name, start_time, end_time, normalized_series
    )

    all_points = []
    for series in normalized_series:
        for point in series.points:
            all_points.append(
                {"timestamp": point.timestamp.isoformat(), "value": point.value}
            )

    all_points.sort(key=lambda x: x["timestamp"])

    claude_client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""
    Analyze this metric data and provide a concise summary:
    
    Metric: {metric_name}
    Time window: {start_time.isoformat()} to {end_time.isoformat()}
    Statistics:
    - Mean: {stats.mean:.4f}
    - Min: {stats.min:.4f}
    - Max: {stats.max:.4f}
    - 95th percentile: {stats.p95:.4f if stats.p95 else 'N/A'}
    - Number of data points: {stats.total_points}
    - Number of time series: {stats.series_count}
    
    Recent data points (last 5):
    {str(all_points[-5:]) if len(all_points) >= 5 else str(all_points)}
    
    Please provide:
    1. A brief summary of the metric behavior
    2. Any noticeable trends (increasing, decreasing, stable)
    3. Potential anomalies or outliers
    4. Business impact assessment (if applicable)
    
    Keep the response concise and focused on actionable insights.
    """

    response = claude_client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=500,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )

    summary_text = response.content[0].text

    anomaly_detection = detect_anomalies(all_points, stats)

    trend = analyze_trend(all_points)

    return {
        "metric_name": metric_name,
        "time_window": TimeWindow(start_time, end_time).to_dict(),
        "statistics": stats.to_dict(),
        "summary": summary_text,
        "has_data": True,
        "anomalies": anomaly_detection,
        "trend": trend,
        "data_points_analyzed": len(all_points),
        "model_used": "claude-3-sonnet-20240229",
    }


def detect_anomalies(points: list, stats: MetricStatistics) -> list:
    """Simple anomaly detection based on statistical thresholds."""
    if not points or stats.mean is None or stats.p95 is None:
        return []

    anomalies = []
    threshold_multiplier = 2.0

    upper_threshold = stats.mean + (stats.p95 - stats.mean) * threshold_multiplier
    lower_threshold = (
        stats.mean
        - (stats.mean - (stats.p95 if stats.p95 else stats.mean)) * threshold_multiplier
    )

    for i, point in enumerate(points[-20:]):
        value = point["value"]

        if value > upper_threshold:
            anomalies.append(
                {
                    "timestamp": point["timestamp"],
                    "value": value,
                    "threshold": upper_threshold,
                    "type": "high",
                    "severity": "high" if value > upper_threshold * 1.5 else "medium",
                }
            )
        elif value < lower_threshold:
            anomalies.append(
                {
                    "timestamp": point["timestamp"],
                    "value": value,
                    "threshold": lower_threshold,
                    "type": "low",
                    "severity": "high" if value < lower_threshold * 0.5 else "medium",
                }
            )

    return anomalies


def analyze_trend(points: list) -> str:
    """Analyze trend direction from recent data points."""
    if len(points) < 10:
        return "insufficient_data"

    recent_points = points[-10:]
    values = [p["value"] for p in recent_points]

    from scipy import stats

    try:
        x = list(range(len(values)))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)

        if abs(slope) < 0.01:
            return "stable"
        elif slope > 0:
            return "increasing"
        else:
            return "decreasing"
    except:
        return "unknown"


if __name__ == "__main__":
    end_time = datetime.now(pytz.UTC)
    start_time = end_time - timedelta(hours=24)

    summary = summarize_metric_trends(
        metric_name="compute.googleapis.com/instance/cpu/utilization",
        start_time=start_time,
        end_time=end_time,
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    )

    print(f"Metric summary: {summary['summary'][:200]}...")
    print(f"Trend: {summary['trend']}")
    print(f"Anomalies detected: {len(summary['anomalies'])}")
