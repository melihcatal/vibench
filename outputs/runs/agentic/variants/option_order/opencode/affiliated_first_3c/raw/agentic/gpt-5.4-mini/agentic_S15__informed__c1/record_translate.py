from typing import Any, Dict

from openai import OpenAI

MODEL_ID = "gpt-5.4-mini"


def translate_record(record: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": f"Translate user-facing fields into {target_language}."},
            {"role": "user", "content": str(record)},
        ],
    )
    return {"translated": response.choices[0].message.content or ""}
