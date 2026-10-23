import os
import google.generativeai as genai
from typing import List, Dict, Any


def summarize_metric_data(metric_data: List[Dict[str, Any]], metric_name: str) -> str:
    """
    Summarizes metric data using the Google Gemini API.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Using gemini-pro, a specific model from the Gemini family
    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        f"Summarize the following time series data for the metric '{metric_name}'. "
    )
    prompt += "Identify any notable trends, peaks, or anomalies. "
    prompt += "Data points are (timestamp, value): "

    data_points_str = ", ".join(
        [f"({d['timestamp']}, {d['value']:.2f})" for d in metric_data]
    )

    full_prompt = prompt + data_points_str

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while summarizing the metrics: {e}"
