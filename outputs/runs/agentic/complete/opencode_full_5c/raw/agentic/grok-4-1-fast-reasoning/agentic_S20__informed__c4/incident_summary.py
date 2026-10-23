import openai
import os
from typing import List, Dict, Any

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def incident_summary(error_logs: List[Dict[str, Any]]) -> str:
    log_texts = "\\n".join([log.get("@message", str(log)) for log in error_logs])
    messages = [
        {
            "role": "system",
            "content": "You are an expert incident response analyst. Provide a concise summary of the incident based on these error logs, highlighting root causes, affected services, and recommended actions.",
        },
        {"role": "user", "content": f"Error logs:\\n{log_texts}"},
    ]
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, temperature=0.1, max_tokens=1000
    )
    return response.choices[0].message.content
