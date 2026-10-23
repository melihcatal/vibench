import os
from typing import List, Dict, Any
from openai import OpenAI

# OpenAI provider
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def incident_summary(error_logs: List[Dict[str, Any]]) -> str:
    """
    Summarize error-log findings for incident review using OpenAI.
    """
    logs_text = "\\n".join(
        log.get("attributes", {}).get("message", str(log)) for log in error_logs
    )
    prompt = f"""Summarize the incident from these error logs:

{logs_text}

Provide: root cause, impact, actions."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()