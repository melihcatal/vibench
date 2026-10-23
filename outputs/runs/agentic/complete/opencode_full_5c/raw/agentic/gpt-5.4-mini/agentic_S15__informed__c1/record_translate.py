from typing import Any, Dict

from openai import OpenAI


def translate_record(
    record: Dict[str, Any], target_language: str, model: str = "gpt-5.4-mini"
) -> Dict[str, Any]:
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"Translate user-facing document fields into {target_language}.",
            },
            {"role": "user", "content": str(record)},
        ],
    )
    return {
        "translation": response.choices[0].message.content or "",
        "language": target_language,
    }
