import os
import openai
import json
from typing import List, Dict, Any


def summarize_incident_logs(log_entries: List[Dict[str, Any]]) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    error_messages = []
    for entry in log_entries:
        attrs = entry.get("attributes", {})
        msg = attrs.get("message", "")
        if msg:
            error_messages.append(msg)
    prompt = f"""Analyze these recent error logs and provide a summary of the incident, including possible root cause, affected services, and recommendations:

{json.dumps(error_messages, indent=2)}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in log analysis for incident response.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.3,
    )
    return response.choices[0].message.content
