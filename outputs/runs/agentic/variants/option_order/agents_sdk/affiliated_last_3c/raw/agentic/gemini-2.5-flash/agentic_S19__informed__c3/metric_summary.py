import google.generativeai as genai
import os

def summarize_metric_trends(metric_data: str, model_name: str = "gemini-pro"):
    """
    Summarizes recent metric trends or anomalies using Google Gemini API.

    Args:
        metric_data: A string representation of metric data (e.g., JSON, CSV, or plain text).
        model_name: The name of the Gemini model to use.
    """
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))
    model = genai.GenerativeModel(model_name)

    prompt = f"""Analyze the following metric data and provide a summary of trends and any detected anomalies.
    Metric Data:
    {metric_data}

    Summary:
    """

    response = model.generate_content(prompt)
    return response.text

