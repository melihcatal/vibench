import os
import json
from openai import OpenAI
from typing import List, Dict


def summarize_error_logs(error_logs: List[Dict]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    log_text = json.dumps(error_logs, indent=2)
    prompt = f"""Analyze these error logs and provide an incident summary.

Include:
- Number of errors
- Common patterns
- Potential root cause
- Recommended actions

Logs:
{log_text}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in log analysis and incident management.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=800,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    sample_errors = [
        {
            "@timestamp": "2024-04-21T10:00:00",
            "level": "ERROR",
            "message": "Database timeout on query users",
        },
        {
            "@timestamp": "2024-04-21T10:01:00",
            "level": "ERROR",
            "message": "Connection pool exhausted",
        },
        {
            "@timestamp": "2024-04-21T10:02:00",
            "level": "ERROR",
            "message": "DB timeout on query orders",
        },
    ]
    summary = summarize_error_logs(sample_errors)
    print(summary)
