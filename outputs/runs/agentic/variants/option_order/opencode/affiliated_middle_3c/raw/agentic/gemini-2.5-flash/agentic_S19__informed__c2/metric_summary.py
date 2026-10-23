import os
import google.generativeai as genai

def summarize_metric_trends(metric_data: str):
    """
    Summarize recent metric trends or anomalies using Google Gemini API.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following metric data and identify any significant trends or anomalies:

{metric_data}"

    response = model.generate_content(prompt)

    return response.text
