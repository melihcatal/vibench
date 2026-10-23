import google.generativeai as genai
from observability_client import get_client_config
from typing import List, Dict, Any


def generate_metric_summary(metric_data: List[Dict[str, Any]], model_name: str = "gemini-1.5-pro") -> str:
    config = get_client_config()
    api_key = config.get("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required for Gemini API.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    
    prompt = (
        "Analyze the following metric data and provide a concise summary of trends, anomalies, "
        "or notable patterns. Include potential root causes if evident.\n\n"
        f"Metric Data: {metric_data}"
    )
    
    response = model.generate_content(prompt)
    return response.text