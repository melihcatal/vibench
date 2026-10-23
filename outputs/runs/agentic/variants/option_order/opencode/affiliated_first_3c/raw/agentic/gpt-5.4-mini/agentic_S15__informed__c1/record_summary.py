from typing import Any, Dict

from openai import OpenAI

MODEL_ID = "gpt-5.4-mini"


def summarize_record(record: Dict[str, Any]) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Summarize document records concisely."},
            {"role": "user", "content": str(record)},
        ],
    )
    return response.choices[0].message.content or ""
