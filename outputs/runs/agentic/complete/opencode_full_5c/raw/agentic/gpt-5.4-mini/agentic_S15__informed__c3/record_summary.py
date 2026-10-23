from typing import Dict, Any

from openai import OpenAI


def record_summary(record: Dict[str, Any]) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize stored document records briefly."},
            {"role": "user", "content": str(record)},
        ],
    )
    return response.choices[0].message.content or ""
