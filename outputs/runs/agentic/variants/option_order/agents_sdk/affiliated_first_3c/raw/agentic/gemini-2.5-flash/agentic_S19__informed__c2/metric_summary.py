import os
import google.generativeai as genai
from typing import List, Dict, Any

def summarize_metric_trends(metric_data: List[Dict[str, Any]], model_name: str = "gemini-pro") -> str:
    """
    Summarizes recent metric trends or anomalies using the Google Gemini API.
    `metric_data` is expected to be a list of dicts, where each dict represents
    a time series or aggregated data point.
    """
    # Ensure GOOGLE_API_KEY is set in environment variables
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel(model_name)

    # Format the metric data into a prompt for the LLM
    prompt = "Please summarize the following metric data, highlighting any significant trends, anomalies, or important observations:

"
    for series in metric_data:
        prompt += f"Resource Labels: {series.get('resource_labels', {})}, "
        prompt += f"Metric Labels: {series.get('metric_labels', {})}
"
        for point in series.get('points', []):
            prompt += f"  Timestamp: {point.get('timestamp')}, Value: {point.get('value')}
"
        prompt += "\n"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing metrics: {e}"
