from typing import Any, Dict

from openai import OpenAI

MODEL_ID = "gpt-5.4-mini"


def assess_text_safety(record: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "Assess document text for unsafe content and return a brief verdict."},
            {"role": "user", "content": str(record)},
        ],
    )
    return {"verdict": response.choices[0].message.content or ""}
