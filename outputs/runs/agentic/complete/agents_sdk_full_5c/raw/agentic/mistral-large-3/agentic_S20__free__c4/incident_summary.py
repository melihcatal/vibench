from typing import List
from openai import OpenAI
import os

def summarize_incident_logs(log_entries: List[dict]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    log_texts = [
        f"{entry.get('timestamp')} {entry.get('severity')}: {entry.get('message')}"
        for entry in log_entries
    ]
    prompt = (
        "Summarize the following log entries for an incident report:\n\n"
        f"{'\\n'.join(log_texts)}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()