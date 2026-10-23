import os
import google.generativeai as genai


def summarize_metric_trends(metric_data):
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        f"Summarize the following metric data for trends or anomalies: {metric_data}"
    )
    response = model.generate_content(prompt)
    return response.text
