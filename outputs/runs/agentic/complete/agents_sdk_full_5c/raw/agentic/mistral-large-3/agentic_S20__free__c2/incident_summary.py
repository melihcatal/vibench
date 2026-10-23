from typing import List
from openai import OpenAI
import os

def summarize_error_logs(log_entries: List[dict]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    if not log_entries:
        return "No error logs provided for summary."
    
    log_texts = [
        f"Timestamp: {entry.get('timestamp')}, Severity: {entry.get('severity')}, "
        f"Message: {entry.get('message')}"
        for entry in log_entries
    ]
    
    prompt = (
        "Summarize the following error logs for an incident report. "
        "Focus on root causes, impacted services, and suggested actions:\n\n"
        f"{'\n'.join(log_texts)}"
    )
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()