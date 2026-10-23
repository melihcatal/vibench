import os
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
import openai


def summarize_metric_trends(
    metric_data: List[Dict[str, Any]], metric_name: str, window_hours: int = 24
) -> str:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")

    client = openai.OpenAI(api_key=openai.api_key)

    summary_data = {
        "metric_name": metric_name,
        "window_hours": window_hours,
        "total_datapoints": len(metric_data),
        "time_range": {
            "start": min(
                [d.get("timestamp", datetime.min) for d in metric_data],
                default=datetime.min,
            ).isoformat(),
            "end": max(
                [d.get("timestamp", datetime.min) for d in metric_data],
                default=datetime.min,
            ).isoformat(),
        }
        if metric_data
        else {},
    }

    if metric_data:
        values = [d.get("value", 0) for d in metric_data]
        summary_data["statistics"] = {
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "trend": "increasing"
            if values[-1] > values[0]
            else "decreasing"
            if values[-1] < values[0]
            else "stable",
        }

    recent_points = metric_data[-10:] if len(metric_data) > 10 else metric_data
    summary_data["recent_values"] = [
        {
            "timestamp": d.get("timestamp", datetime.min).isoformat(),
            "value": d.get("value", 0),
        }
        for d in recent_points
    ]

    prompt = f"""
    Analyze the following metric data and provide a concise summary of trends and potential anomalies:
    
    Metric: {summary_data["metric_name"]}
    Time Window: {summary_data["window_hours"]} hours
    Total Data Points: {summary_data["total_datapoints"]}
    
    Statistics:
    - Mean: {summary_data.get("statistics", {}).get("mean", "N/A")}
    - Min: {summary_data.get("statistics", {}).get("min", "N/A")}
    - Max: {summary_data.get("statistics", {}).get("max", "N/A")}
    - Trend: {summary_data.get("statistics", {}).get("trend", "N/A")}
    
    Recent Values (last 10 points):
    {json.dumps(summary_data.get("recent_values", []), indent=2)}
    
    Provide a summary that includes:
    1. Overall trend analysis
    2. Notable patterns or anomalies
    3. Any potential issues to investigate
    4. Recommendations for monitoring or alerting
    
    Keep the summary concise and actionable.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an observability expert analyzing metric trends. Provide clear, actionable insights.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=500,
        )

        summary = response.choices[0].message.content.strip()

        anomaly_detected = False
        if summary_data.get("statistics"):
            mean = summary_data["statistics"]["mean"]
            max_val = summary_data["statistics"]["max"]
            if max_val > mean * 2:
                anomaly_detected = True

        return {
            "summary": summary,
            "anomaly_detected": anomaly_detected,
            "statistics": summary_data.get("statistics", {}),
            "model_used": "gpt-4",
            "generated_at": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        return {
            "error": str(e),
            "summary": f"Failed to generate summary: {str(e)}",
            "generated_at": datetime.utcnow().isoformat(),
        }


if __name__ == "__main__":
    sample_data = [
        {"timestamp": datetime.utcnow() - timedelta(hours=2), "value": 45.2},
        {"timestamp": datetime.utcnow() - timedelta(hours=1.5), "value": 47.8},
        {"timestamp": datetime.utcnow() - timedelta(hours=1), "value": 52.1},
        {"timestamp": datetime.utcnow() - timedelta(minutes=30), "value": 48.9},
        {"timestamp": datetime.utcnow(), "value": 46.3},
    ]

    result = summarize_metric_trends(sample_data, "cpu_utilization", 3)
    print(f"Summary: {result.get('summary', 'No summary generated')}")
