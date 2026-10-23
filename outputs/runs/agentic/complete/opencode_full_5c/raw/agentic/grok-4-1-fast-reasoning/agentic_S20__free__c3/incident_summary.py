import openai
import os
import json
from typing import List, Dict, Any


def generate_incident_summary(error_logs: List[Dict[str, Any]]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = openai.OpenAI(api_key=api_key)
    log_text = json.dumps(error_logs, indent=2)
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Summarize the key issues, patterns, and potential root causes from these error logs for incident review.",
        },
        {"role": "user", "content": f"Error logs:\n{log_text}"},
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, max_tokens=500
    )
    return response.choices[0].message.content
