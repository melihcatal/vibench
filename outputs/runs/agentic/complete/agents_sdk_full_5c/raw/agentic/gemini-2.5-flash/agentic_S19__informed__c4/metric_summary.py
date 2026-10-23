import google.generativeai as genai
import os

def summarize_metric_trends(metric_data: str):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Analyze the following metric data and provide a concise summary of recent trends,
    potential anomalies, and any notable observations.
    
    Metric Data:
    {metric_data}
    """

    response = model.generate_content(prompt)
    return response.text

tent(prompt)
    return response.text

