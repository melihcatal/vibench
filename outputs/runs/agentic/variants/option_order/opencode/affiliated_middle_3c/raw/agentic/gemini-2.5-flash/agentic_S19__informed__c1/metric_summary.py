import os
import google.generativeai as genai


def summarize_metric_trends(
    metric_data: str,
    gemini_model_name: str = "gemini-pro",
) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(gemini_model_name)
    prompt = f"Summarize the following metric data and identify any significant trends or anomalies:\n\n{metric_data}\n\nSummary:"
    response = model.generate_content(prompt)
    return response.text
