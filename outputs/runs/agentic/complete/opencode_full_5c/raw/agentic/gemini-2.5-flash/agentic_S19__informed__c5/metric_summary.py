import os
import google.generativeai as genai


def summarize_metric_trends(metric_data: list) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for text generation

    # Prepare the metric data for the LLM
    # This is a simplified representation, a real scenario might require more sophisticated data preparation
    data_summary = ""
    for item in metric_data:
        data_summary += f"Metric Type: {item.get('metric_type')}, Resource Type: {item.get('resource_type')}, Time: {item.get('end_time')}, Value: {item.get('value')}\n"

    prompt = f"""Analyze the following metric data and provide a concise summary of recent trends or anomalies. 
               Focus on identifying patterns, significant changes, or unusual values. 
               Here is the data: {data_summary}"""

    response = model.generate_content(prompt)
    return response.text
