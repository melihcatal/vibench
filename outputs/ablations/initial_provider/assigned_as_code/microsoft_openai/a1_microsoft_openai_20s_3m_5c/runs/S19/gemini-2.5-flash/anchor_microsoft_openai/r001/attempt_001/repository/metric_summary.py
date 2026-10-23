import os
import google.generativeai as genai

def summarize_metric_trends(payload):
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    metric_data_str = ""
    for point in payload.get('metric_data', []):
        metric_data_str += f"Timestamp: {point['timestamp']}, Value: {point['value']}\n"

    prompt = f"Summarize the following metric data and identify any trends or anomalies:\n\n{metric_data_str}"
    
    response = model.generate_content(prompt)
    return {'summary': response.text}
