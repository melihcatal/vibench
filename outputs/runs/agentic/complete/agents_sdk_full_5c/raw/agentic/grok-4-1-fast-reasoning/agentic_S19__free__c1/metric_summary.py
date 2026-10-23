import openai
import os
import json
from typing import List, Dict, Any

def summarize_recent_metric_trends(datapoints: List[Dict[str, Any]]) -> str:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    data_str = json.dumps(datapoints[-100:], indent=2)  # recent 100 points
    messages = [
        {"role": "system", "content": "You are an expert metrics monitoring analyst. Identify key trends, averages, peaks, drops, and potential anomalies."},
        {"role": "user", "content": f"Analyze and summarize the metric data:\n{data_str}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=500
    )
    return response.choices[0].message.content
