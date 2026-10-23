import os
from datetime import datetime, timedelta
import openai
from typing import Dict, Any, List


def summarize_metric_trends(
    metric_data: List[Dict[str, Any]], metric_name: str
) -> Dict[str, Any]:
    """
    Summarize recent metric trends or anomalies using OpenAI GPT.

    Args:
        metric_data: List of metric datapoints from query_metric_window
        metric_name: Name of the metric being analyzed

    Returns:
        Dictionary with summary, trends, and anomaly detection
    """
    if not metric_data:
        return {
            "summary": "No data available for analysis",
            "trends": [],
            "anomalies": [],
            "confidence": 0.0,
        }

    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    values = [point["value"] for point in metric_data if point["value"] is not None]
    timestamps = [point["timestamp"] for point in metric_data]

    if not values:
        return {
            "summary": "No numeric values available for analysis",
            "trends": [],
            "anomalies": [],
            "confidence": 0.0,
        }

    min_val = min(values)
    max_val = max(values)
    avg_val = sum(values) / len(values)

    sorted_values = sorted(values)
    p95 = (
        sorted_values[int(len(values) * 0.95) - 1]
        if len(values) >= 2
        else sorted_values[0]
    )

    recent_values = values[-10:] if len(values) >= 10 else values
    recent_avg = sum(recent_values) / len(recent_values)

    trend = "stable"
    if recent_avg > avg_val * 1.2:
        trend = "increasing"
    elif recent_avg < avg_val * 0.8:
        trend = "decreasing"

    anomalies = []
    threshold = p95 * 1.5

    for i, (point, value) in enumerate(zip(metric_data, values)):
        if value > threshold:
            anomalies.append(
                {
                    "timestamp": point["timestamp"],
                    "value": value,
                    "threshold": threshold,
                    "deviation": ((value - avg_val) / avg_val * 100)
                    if avg_val != 0
                    else float("inf"),
                }
            )

    prompt = f"""
    Analyze the following metric data for {metric_name}:
    
    - Total datapoints: {len(values)}
    - Time range: {timestamps[0]} to {timestamps[-1]}
    - Average value: {avg_val:.4f}
    - Minimum value: {min_val:.4f}
    - Maximum value: {max_val:.4f}
    - 95th percentile: {p95:.4f}
    - Recent trend: {trend}
    - Anomalies detected: {len(anomalies)}
    
    Provide a concise summary of the metric behavior, including:
    1. Overall health and performance
    2. Notable trends or patterns
    3. Any concerning anomalies
    4. Recommendations for monitoring or investigation
    
    Keep the summary under 200 words.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a monitoring and observability expert analyzing metric data.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.3,
        )

        ai_summary = response.choices[0].message.content.strip()

    except Exception as e:
        ai_summary = f"AI analysis unavailable: {str(e)}"

    summary_data = {
        "metric": metric_name,
        "datapoint_count": len(values),
        "time_range": {
            "start": timestamps[0].isoformat()
            if isinstance(timestamps[0], datetime)
            else str(timestamps[0]),
            "end": timestamps[-1].isoformat()
            if isinstance(timestamps[-1], datetime)
            else str(timestamps[-1]),
        },
        "statistics": {
            "average": avg_val,
            "minimum": min_val,
            "maximum": max_val,
            "p95": p95,
            "recent_trend": trend,
        },
        "anomalies": {
            "count": len(anomalies),
            "threshold": threshold,
            "details": anomalies[:5],
        },
        "ai_summary": ai_summary,
        "confidence": min(0.95, 1.0 - (len(anomalies) / max(len(values), 1)) * 0.5),
    }

    return summary_data


if __name__ == "__main__":
    sample_data = [
        {
            "timestamp": datetime.utcnow() - timedelta(minutes=i),
            "value": 0.5 + (i % 10) * 0.1,
            "metric_type": "compute.googleapis.com/instance/cpu/utilization",
            "resource_type": "gce_instance",
            "resource_labels": {"instance_id": "test-instance"},
        }
        for i in range(60, 0, -1)
    ]

    try:
        summary = summarize_metric_trends(
            sample_data, "compute.googleapis.com/instance/cpu/utilization"
        )
        print(f"Metric Summary for {summary['metric']}:")
        print(f"  Datapoints: {summary['datapoint_count']}")
        print(f"  Average: {summary['statistics']['average']:.4f}")
        print(f"  Trend: {summary['statistics']['recent_trend']}")
        print(f"  Anomalies: {summary['anomalies']['count']}")
        print(f"  Confidence: {summary['confidence']:.2f}")
        print(f"\nAI Summary:\n{summary['ai_summary']}")
    except Exception as e:
        print(f"Error summarizing metric trends: {e}")
