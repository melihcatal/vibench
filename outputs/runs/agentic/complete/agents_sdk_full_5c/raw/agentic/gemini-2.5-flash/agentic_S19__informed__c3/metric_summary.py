import os
import google.generativeai as genai

def summarize_metric_trends(metric_data: str, additional_context: str = None) -> str:
    """
    Summarizes recent metric trends or anomalies using the Google Gemini API.

    Args:
        metric_data: A string representation of the metric data (e.g., JSON or text).
        additional_context: Any additional context to provide to the LLM.

    Returns:
        A string summarizing the metric trends or anomalies.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = (
        "Analyze the following metric data and summarize any significant trends, "
        "anomalies, or observations. "
    )
    if additional_context:
        prompt += f"Consider the following context: {additional_context}. "
    prompt += f"Metric data: {metric_data}"

    response = model.generate_content(prompt)

    return response.text

