import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os

def summarize_metric_trends(metric_data: dict, config: dict = None) -> dict:
    config = config or {}
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = (
        "Analyze the following metric data and summarize recent trends or anomalies. "
        "Provide a concise summary highlighting any significant changes, spikes, dips, or patterns.

"
        f"Metric Data: {metric_data}

Summary:"
    )

    response = model.generate_content(
        prompt,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    return {'summary': response.text}
