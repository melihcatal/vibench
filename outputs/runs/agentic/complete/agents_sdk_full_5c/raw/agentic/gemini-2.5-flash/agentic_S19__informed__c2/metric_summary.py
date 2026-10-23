import google.generativeai as genai
import os

def summarize_metric_trends(metric_data: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro') # Using a concrete model identifier

    prompt = f"""Summarize the following metric data, highlighting any trends, anomalies, or significant changes:

{metric_data}

Summary:"""

    response = model.generate_content(prompt)
    return response.text
