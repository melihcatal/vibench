import os
import google.generativeai as genai
from observability_models import MetricQueryResult
from typing import List


def summarize_metric_trends(metric_data: List[MetricQueryResult]) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        "Summarize the following metric data and highlight any trends or anomalies:\n"
    )
    for data_point in metric_data:
        prompt += f"Time: {data_point.time}, Value: {data_point.value}, Labels: {data_point.labels}\n"

    response = model.generate_content(prompt)
    return response.text
