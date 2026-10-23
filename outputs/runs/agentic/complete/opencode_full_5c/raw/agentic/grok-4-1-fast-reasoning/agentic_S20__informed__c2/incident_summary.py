import openai
import os
from typing import List, Dict, Any

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def incident_summary(error_logs: List[Dict[str, Any]]) -> str:
    logs_text = "\n".join([log.get("message", str(log)) for log in error_logs])
    prompt = f"""Summarize the incident based on these error logs:

{logs_text}

Provide a concise summary, potential root cause, and affected components."""
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert incident analyst reviewing application logs.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
