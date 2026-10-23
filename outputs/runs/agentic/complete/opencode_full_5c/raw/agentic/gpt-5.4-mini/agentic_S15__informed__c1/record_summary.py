from typing import Any, Dict

from openai import OpenAI


def summarize_record(record: Dict[str, Any], model: str = "gpt-5.4-mini") -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Summarize document records concisely."},
            {"role": "user", "content": str(record)},
        ],
    )
    return response.choices[0].message.content or ""
