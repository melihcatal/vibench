import os
import google.generativeai as genai
from typing import List
from observability_models import TimeSeries


def summarize_metric_data(time_series_data: List[TimeSeries]) -> str:
    """
    Summarizes metric data using the Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = "Summarize the following metric data and identify any potential anomalies or interesting trends:\n\n"
    for series in time_series_data:
        prompt += f"Metric: {series.metric_name}\n"
        prompt += f"Resource: {series.resource_labels}\n"
        points_str = ", ".join(
            [f"({p.timestamp.isoformat()}: {p.value:.2f})" for p in series.points]
        )
        prompt += f"Data points: {points_str}\n\n"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary from Gemini API: {e}"
