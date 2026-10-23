import os
from typing import Dict, Any
import anthropic


def summarize_metric_trends(metric_data: Dict[str, Any]) -> str:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    metric_name = metric_data.get("metric_name", "unknown")
    values = metric_data.get("values", [])
    timestamps = metric_data.get("timestamps", [])
    labels = metric_data.get("labels", {})

    if not values:
        return "No metric data available for analysis"

    value_str = ", ".join([str(v) for v in values[-10:]])
    label_str = ", ".join([f"{k}: {v}" for k, v in labels.items()])

    prompt = f"""You are analyzing metric data from a monitoring system. Provide a concise summary of trends and potential anomalies.

Metric: {metric_name}
Recent values (last 10): {value_str}
Labels: {label_str}
Number of data points: {len(values)}

Please analyze this metric data and provide:
1. A brief summary of the trend (increasing, decreasing, stable, volatile)
2. Any noticeable patterns or anomalies
3. Potential implications or recommendations

Keep the response concise and focused on observability insights."""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def detect_metric_anomalies(metric_data: Dict[str, Any]) -> Dict[str, Any]:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    values = metric_data.get("values", [])
    if len(values) < 5:
        return {"anomalies": [], "confidence": 0.0, "reason": "Insufficient data"}

    value_str = ", ".join([str(v) for v in values])

    prompt = f"""Analyze this time series metric data for anomalies. The values are: {value_str}

Identify any statistical anomalies, outliers, or unusual patterns. Consider:
1. Sudden spikes or drops
2. Changes in variance or volatility
3. Deviations from expected patterns
4. Potential data quality issues

Return a JSON object with:
- anomalies: list of indices where anomalies occur
- confidence: confidence score (0-1)
- reason: brief explanation of anomalies detected
- severity: low/medium/high for each anomaly"""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )

        import json

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {
                "anomalies": [],
                "confidence": 0.0,
                "reason": "Could not parse AI response",
                "raw_response": response.content[0].text,
            }
    except Exception as e:
        return {"anomalies": [], "confidence": 0.0, "reason": f"Error: {str(e)}"}
