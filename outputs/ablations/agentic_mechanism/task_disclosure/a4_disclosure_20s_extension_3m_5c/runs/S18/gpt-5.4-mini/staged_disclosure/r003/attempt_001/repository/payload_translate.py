import os
from typing import Any, Dict, List, Union

from openai import OpenAI


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _translate_text(text: str, target_language: str) -> str:
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": f"Translate customer-facing text into {target_language}. Preserve meaning, tone, placeholders, and formatting. Return only the translated text.",
            },
            {"role": "user", "content": text},
        ],
    )
    return response.output_text.strip()


def translate_payload(payload: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    def transform(value: Any) -> Any:
        if isinstance(value, str):
            return _translate_text(value, target_language)
        if isinstance(value, list):
            return [transform(item) for item in value]
        if isinstance(value, dict):
            return {key: transform(item) for key, item in value.items()}
        return value

    return transform(payload)
