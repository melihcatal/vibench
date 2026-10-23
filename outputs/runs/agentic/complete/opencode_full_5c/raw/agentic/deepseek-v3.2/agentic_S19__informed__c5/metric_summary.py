import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from datetime import datetime


def summarize_metric_trends(
    metric_data: List[Dict[str, Any]],
    metric_name: str,
    window_start: datetime,
    window_end: datetime,
) -> Dict[str, Any]:
    """
    Summarize recent metric trends or anomalies using Google Gemini API.

    Args:
        metric_data: List of metric data points
        metric_name: Name of the metric being analyzed
        window_start: Start of analysis window
        window_end: End of analysis window

    Returns:
        Dictionary with summary and analysis
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set")

    genai.configure(api_key=api_key)

    if not metric_data:
        return {
            "metric": metric_name,
            "window": {
                "start": window_start.isoformat(),
                "end": window_end.isoformat(),
            },
            "summary": "No metric data available for analysis",
            "trend": "insufficient_data",
            "anomalies": [],
            "recommendations": [],
        }

    values = [point.get("value", 0) for point in metric_data if "value" in point]
    timestamps = [
        point.get("timestamp", "") for point in metric_data if "timestamp" in point
    ]

    if not values:
        return {
            "metric": metric_name,
            "window": {
                "start": window_start.isoformat(),
                "end": window_end.isoformat(),
            },
            "summary": "No valid metric values found",
            "trend": "insufficient_data",
            "anomalies": [],
            "recommendations": [],
        }

    avg_value = sum(values) / len(values)
    max_value = max(values)
    min_value = min(values)

    data_summary = f"""
    Metric Analysis for: {metric_name}
    Analysis Window: {window_start.isoformat()} to {window_end.isoformat()}
    Data Points: {len(values)}
    Average Value: {avg_value:.4f}
    Maximum Value: {max_value:.4f}
    Minimum Value: {min_value:.4f}
    Value Range: {max_value - min_value:.4f}
    
    Recent Values (last 5): {values[-5:] if len(values) >= 5 else values}
    """

    prompt = f"""
    You are a cloud monitoring analyst. Analyze the following metric data and provide:
    1. A concise summary of the metric trend
    2. Identification of any anomalies or unusual patterns
    3. Recommendations for action if needed
    
    {data_summary}
    
    Please provide your analysis in the following JSON format:
    {{
        "summary": "brief summary of the trend",
        "trend": "increasing|decreasing|stable|volatile",
        "anomalies": ["list", "of", "anomalies", "if", "any"],
        "recommendations": ["list", "of", "recommendations"]
    }}
    
    Only respond with valid JSON.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)

        import json

        analysis_result = json.loads(response.text.strip())

        result = {
            "metric": metric_name,
            "window": {
                "start": window_start.isoformat(),
                "end": window_end.isoformat(),
            },
            "data_points": len(values),
            "statistics": {
                "average": avg_value,
                "maximum": max_value,
                "minimum": min_value,
                "range": max_value - min_value,
            },
            "summary": analysis_result.get("summary", ""),
            "trend": analysis_result.get("trend", "unknown"),
            "anomalies": analysis_result.get("anomalies", []),
            "recommendations": analysis_result.get("recommendations", []),
            "model_used": "gemini-1.5-pro",
        }

        return result

    except Exception as e:
        raise RuntimeError(
            f"Failed to summarize metric trends with Gemini API: {str(e)}"
        )
