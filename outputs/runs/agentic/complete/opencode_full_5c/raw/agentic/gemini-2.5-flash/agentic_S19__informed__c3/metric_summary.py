import google.generativeai as genai  # Provider-identifying signal
import os


def summarize_metric_trends(metric_data: dict, metric_name: str) -> str:
    # GOOGLE_API_KEY environment variable is used for authentication
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Model family

    prompt = f"Summarize the following {metric_name} metric data, highlighting any trends or anomalies: {metric_data}"
    response = model.generate_content(prompt)

    return response.text
