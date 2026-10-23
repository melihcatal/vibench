import os
import google.generativeai as genai
from observability_models import MetricTimeSeries


def summarize_metric(series: MetricTimeSeries) -> str:
    """
    Summarizes metric trends or anomalies using Google's Gemini model.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Summarize the following time series data for the metric '{series.metric_name}'.
    Identify any notable trends, spikes, or anomalies.
    Dimensions: {series.dimensions}
    Data points (timestamp, value):
    """
    for point in series.points:
        prompt += f"({point.timestamp}, {point.value})\n"

    response = model.generate_content(prompt)
    return response.text
