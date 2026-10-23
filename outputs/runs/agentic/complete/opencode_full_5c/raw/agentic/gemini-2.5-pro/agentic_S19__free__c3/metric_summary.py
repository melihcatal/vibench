import os
import google.generativeai as genai
from observability_models import MetricData, MetricSummary, MetricSummaryRequest
from typing import List


def summarize_metrics(request: MetricSummaryRequest) -> MetricSummary:
    """
    Summarizes metric data using the Gemini API.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = "Summarize the following metric data. Highlight any anomalies or important trends:\n\n"
    for data in request.metric_data:
        prompt += f"Metric: {data.metric_name}\n"
        if data.dimensions:
            prompt += f"Dimensions: {data.dimensions}\n"
        for point in data.points:
            prompt += f"  - Time: {point.timestamp}, Value: {point.value}\n"
        prompt += "\n"

    response = model.generate_content(prompt)
    return MetricSummary(summary=response.text)
