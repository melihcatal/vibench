import google.generativeai as genai
import os


def summarize_metric_trends(metric_data: str) -> str:
    # GOOGLE_API_KEY environment variable should be set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""Analyze the following metric data and summarize recent trends or anomalies. 
    Focus on identifying patterns, significant changes, or unusual observations. 
    Here is the metric data: {metric_data}
    """

    response = model.generate_content(prompt)
    return response.text
