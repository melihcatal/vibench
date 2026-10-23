import os
import google.generativeai as genai

def summarize_metric_trends(metric_data_description: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = (
        f"Summarize the following metric trends and identify any anomalies. "
        f"Provide a concise summary:

{metric_data_description}"
    )
    response = model.generate_content(prompt)
    return response.text
