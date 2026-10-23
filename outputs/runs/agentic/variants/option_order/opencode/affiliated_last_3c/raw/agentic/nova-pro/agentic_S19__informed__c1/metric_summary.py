import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

from google.generativeai import GenerativeModel


def metric_summary(metric_data):
    model = GenerativeModel("models/gemini-1.5-pro-latest")
    prompt = f"Summarize the following metric data: {metric_data}"
    response = model.generate_content(prompt)
    return response.text
