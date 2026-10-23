import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import statistics
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import google.api_core.exceptions
from openai import OpenAI


def summarize_metric_trends(
    metric_name: str,
    project_id: str,
    start_time: datetime,
    end_time: datetime,
    filters: Optional[Dict[str, str]] = None,
    anomaly_threshold_stddev: float = 2.0,
) -> Dict[str, Any]:
    """
    Summarize recent metric trends or anomalies using Google Cloud Monitoring and OpenAI.

    Args:
        metric_name: The metric type name (e.g., 'compute.googleapis.com/instance/cpu/utilization')
        project_id: Google Cloud project ID
        start_time: Start of time window
        end_time: End of time window
        filters: Optional resource or metric label filters
        anomaly_threshold_stddev: Standard deviation threshold for anomaly detection

    Returns:
        Dictionary containing trend summary and analysis
    """
    from .query_metric_window import query_metric_window

    try:
        datapoints = query_metric_window(
            metric_name=metric_name,
            project_id=project_id,
            start_time=start_time,
            end_time=end_time,
            filter_labels=filters,
        )

        if not datapoints:
            return {
                "metric_name": metric_name,
                "time_window": {"start": start_time, "end": end_time},
                "summary": "No data available for the specified time window",
                "statistics": {},
                "anomalies": [],
                "trend_analysis": {},
            }

        values = [dp["value"] for dp in datapoints if dp["value"] is not None]
        timestamps = [dp["timestamp"] for dp in datapoints if dp["value"] is not None]

        if not values:
            return {
                "metric_name": metric_name,
                "time_window": {"start": start_time, "end": end_time},
                "summary": "No valid numeric values in the time window",
                "statistics": {},
                "anomalies": [],
                "trend_analysis": {},
            }

        stats = {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "stddev": statistics.stdev(values) if len(values) > 1 else 0.0,
            "sum": sum(values),
        }

        anomalies = detect_anomalies(
            values, timestamps, stats["mean"], stats["stddev"], anomaly_threshold_stddev
        )

        trend_analysis = analyze_trend(values, timestamps)

        summary_text = generate_summary_text(
            metric_name=metric_name,
            stats=stats,
            trend_analysis=trend_analysis,
            anomalies=anomalies,
            time_window={"start": start_time, "end": end_time},
        )

        return {
            "metric_name": metric_name,
            "time_window": {"start": start_time, "end": end_time},
            "filters": filters or {},
            "summary": summary_text,
            "statistics": stats,
            "anomalies": anomalies,
            "trend_analysis": trend_analysis,
            "data_points_count": len(datapoints),
            "valid_values_count": len(values),
        }

    except Exception as e:
        print(f"Error summarizing metric trends: {e}")
        raise


def detect_anomalies(
    values: List[float],
    timestamps: List[datetime],
    mean: float,
    stddev: float,
    threshold_stddev: float,
) -> List[Dict[str, Any]]:
    """
    Detect anomalies in metric values.

    Args:
        values: List of metric values
        timestamps: Corresponding timestamps
        mean: Mean value
        stddev: Standard deviation
        threshold_stddev: Threshold in standard deviations

    Returns:
        List of detected anomalies
    """
    if stddev == 0:
        return []

    threshold = threshold_stddev * stddev
    anomalies = []

    for i, (value, timestamp) in enumerate(zip(values, timestamps)):
        deviation = abs(value - mean)
        if deviation > threshold:
            z_score = (value - mean) / stddev
            anomaly_type = "high" if value > mean else "low"

            anomalies.append(
                {
                    "timestamp": timestamp,
                    "value": value,
                    "deviation": deviation,
                    "z_score": z_score,
                    "type": anomaly_type,
                    "severity": "critical"
                    if abs(z_score) > 3
                    else "warning"
                    if abs(z_score) > 2
                    else "minor",
                    "position": i,
                }
            )

    return anomalies


def analyze_trend(values: List[float], timestamps: List[datetime]) -> Dict[str, Any]:
    """
    Analyze trend in metric values.

    Args:
        values: List of metric values
        timestamps: Corresponding timestamps

    Returns:
        Trend analysis results
    """
    if len(values) < 2:
        return {"trend": "insufficient_data", "slope": 0, "r_squared": 0}

    from scipy import stats
    import numpy as np

    time_numeric = np.array([ts.timestamp() for ts in timestamps])
    values_array = np.array(values)

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        time_numeric, values_array
    )

    r_squared = r_value**2

    if slope > 0.01:
        trend = "increasing"
    elif slope < -0.01:
        trend = "decreasing"
    else:
        trend = "stable"

    first_half_mean = (
        statistics.mean(values[: len(values) // 2]) if len(values) >= 4 else None
    )
    second_half_mean = (
        statistics.mean(values[len(values) // 2 :]) if len(values) >= 4 else None
    )

    percent_change = None
    if first_half_mean and second_half_mean and first_half_mean != 0:
        percent_change = ((second_half_mean - first_half_mean) / first_half_mean) * 100

    volatility = (
        np.std(values_array) / np.mean(values_array)
        if np.mean(values_array) != 0
        else 0
    )

    return {
        "trend": trend,
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_squared,
        "p_value": p_value,
        "percent_change": percent_change,
        "volatility": volatility,
        "first_half_mean": first_half_mean,
        "second_half_mean": second_half_mean,
    }


def generate_summary_text(
    metric_name: str,
    stats: Dict[str, Any],
    trend_analysis: Dict[str, Any],
    anomalies: List[Dict[str, Any]],
    time_window: Dict[str, datetime],
) -> str:
    """
    Generate human-readable summary text using OpenAI.

    Args:
        metric_name: Metric name
        stats: Statistics dictionary
        trend_analysis: Trend analysis results
        anomalies: List of anomalies
        time_window: Time window dictionary

    Returns:
        Summary text
    """
    try:
        openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not openai_api_key:
            return generate_basic_summary(
                metric_name, stats, trend_analysis, anomalies, time_window
            )

        client = OpenAI(api_key=openai_api_key)

        duration_hours = (
            time_window["end"] - time_window["start"]
        ).total_seconds() / 3600

        prompt = f"""
        Analyze this metric data and provide a concise summary:
        
        Metric: {metric_name}
        Time window: {duration_hours:.1f} hours
        Data points: {stats.get("count", 0)}
        
        Statistics:
        - Mean: {stats.get("mean", 0):.3f}
        - Median: {stats.get("median", 0):.3f}
        - Min: {stats.get("min", 0):.3f}
        - Max: {stats.get("max", 0):.3f}
        - Std Dev: {stats.get("stddev", 0):.3f}
        
        Trend Analysis:
        - Trend: {trend_analysis.get("trend", "unknown")}
        - Slope: {trend_analysis.get("slope", 0):.6f}
        - R-squared: {trend_analysis.get("r_squared", 0):.3f}
        - Percent change: {trend_analysis.get("percent_change", 0):.1f}%
        
        Anomalies detected: {len(anomalies)}
        
        Provide a 3-4 sentence summary focusing on:
        1. Overall performance level
        2. Trend direction and significance
        3. Any concerning anomalies
        4. Key takeaway for monitoring
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful observability analyst. Provide clear, concise summaries of metric data.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"OpenAI summary generation failed: {e}")
        return generate_basic_summary(
            metric_name, stats, trend_analysis, anomalies, time_window
        )


def generate_basic_summary(
    metric_name: str,
    stats: Dict[str, Any],
    trend_analysis: Dict[str, Any],
    anomalies: List[Dict[str, Any]],
    time_window: Dict[str, datetime],
) -> str:
    """Generate basic summary without OpenAI."""
    duration_hours = (time_window["end"] - time_window["start"]).total_seconds() / 3600

    summary_parts = []

    summary_parts.append(f"Metric '{metric_name}' over {duration_hours:.1f} hours:")
    summary_parts.append(
        f"Average: {stats.get('mean', 0):.3f} (range: {stats.get('min', 0):.3f}-{stats.get('max', 0):.3f})"
    )

    trend = trend_analysis.get("trend", "unknown")
    if trend != "insufficient_data":
        summary_parts.append(
            f"Trend: {trend} (slope: {trend_analysis.get('slope', 0):.6f})"
        )

    if anomalies:
        critical_count = sum(1 for a in anomalies if a.get("severity") == "critical")
        warning_count = sum(1 for a in anomalies if a.get("severity") == "warning")
        summary_parts.append(
            f"Anomalies: {len(anomalies)} total ({critical_count} critical, {warning_count} warnings)"
        )

    return " ".join(summary_parts)


def get_metric_health_score(
    metric_name: str, project_id: str, lookback_hours: int = 24
) -> Dict[str, Any]:
    """
    Calculate a health score for a metric based on recent data.

    Args:
        metric_name: Metric type name
        project_id: Google Cloud project ID
        lookback_hours: Hours to look back

    Returns:
        Health score and analysis
    """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=lookback_hours)

    summary = summarize_metric_trends(
        metric_name=metric_name,
        project_id=project_id,
        start_time=start_time,
        end_time=end_time,
        anomaly_threshold_stddev=2.0,
    )

    stats = summary.get("statistics", {})
    trend_analysis = summary.get("trend_analysis", {})
    anomalies = summary.get("anomalies", [])

    health_score = 100

    if anomalies:
        critical_anomalies = sum(
            1 for a in anomalies if a.get("severity") == "critical"
        )
        warning_anomalies = sum(1 for a in anomalies if a.get("severity") == "warning")

        health_score -= critical_anomalies * 20
        health_score -= warning_anomalies * 5
        health_score = max(health_score, 0)

    trend = trend_analysis.get("trend", "stable")
    if trend == "increasing" and stats.get("mean", 0) > 80:
        health_score -= 10
    elif trend == "decreasing" and stats.get("mean", 0) < 20:
        health_score -= 10

    volatility = trend_analysis.get("volatility", 0)
    if volatility > 0.5:
        health_score -= 15

    health_status = (
        "healthy"
        if health_score >= 80
        else "degraded"
        if health_score >= 60
        else "unhealthy"
    )

    return {
        "metric_name": metric_name,
        "health_score": health_score,
        "health_status": health_status,
        "factors": {
            "anomaly_count": len(anomalies),
            "trend": trend,
            "volatility": volatility,
            "mean_value": stats.get("mean", 0),
        },
        "recommendations": generate_health_recommendations(health_score, summary),
    }


def generate_health_recommendations(
    health_score: int, summary: Dict[str, Any]
) -> List[str]:
    """Generate recommendations based on health score."""
    recommendations = []

    if health_score < 60:
        recommendations.append(
            "Investigate immediately - metric shows unhealthy patterns"
        )

    anomalies = summary.get("anomalies", [])
    if anomalies:
        recommendations.append(f"Review {len(anomalies)} detected anomalies")

    trend = summary.get("trend_analysis", {}).get("trend", "stable")
    if trend == "increasing" and summary.get("statistics", {}).get("mean", 0) > 70:
        recommendations.append(
            "Consider scaling resources - metric shows increasing trend at high levels"
        )
    elif trend == "decreasing" and summary.get("statistics", {}).get("mean", 0) < 30:
        recommendations.append(
            "Check for underutilization - metric shows decreasing trend at low levels"
        )

    return recommendations
