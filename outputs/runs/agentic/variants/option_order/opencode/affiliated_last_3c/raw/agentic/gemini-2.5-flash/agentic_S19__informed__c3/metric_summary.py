import os
import google.generativeai as genai
from typing import List
from observability_models import MetricDataPoint

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def summarize_metric_trends(metric_name: str, datapoints: List[MetricDataPoint]) -> str:
    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Using gemini-pro as a concrete model identifier

    # Prepare the data for the LLM
    data_string = ""
    for dp in datapoints:
        data_string += (
            f"Timestamp: {dp.timestamp}, Value: {dp.value}, Labels: {dp.labels}\n"
        )

    prompt = f"""Analyze the following metric data for '{metric_name}' and provide a concise summary of recent trends or anomalies. Focus on significant changes, patterns, or unusual observations. If no specific trends are observed, state that.

Metric Data:
{data_string}

Summary:"""

    response = model.generate_content(prompt)
    return response.text
