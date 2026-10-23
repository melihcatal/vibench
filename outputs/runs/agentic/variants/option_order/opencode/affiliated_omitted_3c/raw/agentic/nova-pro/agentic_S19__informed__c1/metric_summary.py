import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

from google.generativeai import GenerativeModel


def metric_summary(metric_name):
    model = GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(
        f"Summarize the recent trends or anomalies for the metric {metric_name}"
    )
    return response.text
