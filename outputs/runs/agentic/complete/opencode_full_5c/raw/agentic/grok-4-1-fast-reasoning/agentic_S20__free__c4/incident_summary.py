import os
import openai
from typing import List
from observability_models import LogEntry


def summarize_incident(log_entries: List[LogEntry]) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    log_summary = "\n".join(
        f"[{entry.timestamp}] {entry.level}: {entry.message}" for entry in log_entries
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes incidents from log entries.",
            },
            {"role": "user", "content": f"Summarize the incident:\n{log_summary}"},
        ],
    )
    return response.choices[0].message.content
