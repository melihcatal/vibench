import google.generativeai as genai
import os
from typing import List, Dict, Any

def summarize_metric_trends(metric_data: List[Dict[str, Any]], model_name: str = "gemini-pro") -> str:
    """
    Summarizes recent metric trends or anomalies using the Google Gemini API.
    Assumes GOOGLE_API_KEY is set in environment variables.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel(model_name)

    prompt = f"Summarize the following metric data, highlighting any significant trends or anomalies:

{metric_data}"

    response = model.generate_content(prompt)
    return response.text
