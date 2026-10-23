from typing import List
from openai import OpenAI
import os

def summarize_error_logs_for_incident(logs: List[dict]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    log_texts = "\n".join([f"{log.get('message', '')} - {log.get('attributes', {})}" for log in logs])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize these error logs for an incident report."},
            {"role": "user", "content": log_texts}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()