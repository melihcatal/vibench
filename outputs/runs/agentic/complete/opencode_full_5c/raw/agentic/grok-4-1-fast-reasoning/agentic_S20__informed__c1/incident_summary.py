import openai
import os
from typing import List, Dict, Any

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_incident(error_logs: List[Dict[str, Any]]) -> str:
    logs_text = "\n".join(
        [
            f"[{log['timestamp']}] {log['level']}: {log['message']} (trace_id: {log.get('trace_id', 'N/A')})"
            for log in error_logs
        ]
    )
    prompt = f"""Summarize the following error logs for incident review:

{logs_text}

Provide:
- Summary of the issue
- Affected components/services
- Potential root cause
- Recommended next steps"""

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a log analysis expert."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content
