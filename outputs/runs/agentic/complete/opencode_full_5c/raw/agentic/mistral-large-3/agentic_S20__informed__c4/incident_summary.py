import os
from openai import OpenAI
from typing import List, Dict


def incident_summary(error_logs: List[Dict[str, str]]) -> str:
    """Summarize error-log findings for incident review using OpenAI GPT."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    log_messages = "\n".join(
        [
            f"Timestamp: {log.get('timestamp')}, Severity: {log.get('severity')}, Message: {log.get('message')}"
            for log in error_logs
        ]
    )

    prompt = (
        "Summarize the following error logs for an incident review. "
        "Focus on the root cause, impact, and suggested actions:\n\n"
        f"{log_messages}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Failed to generate incident summary using OpenAI: {e}")
        raise
