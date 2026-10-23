import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-5.4-mini")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _stringify_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def translate_record(record: Dict[str, Any], target_language: str, fields: Optional[List[str]] = None) -> Dict[str, Any]:
    if not isinstance(record, dict):
        raise TypeError("record must be a dictionary")
    if not target_language or not isinstance(target_language, str):
        raise ValueError("target_language must be a non-empty string")

    selected_fields = fields or [k for k, v in record.items() if isinstance(v, str) and v.strip()]
    if not selected_fields:
        return dict(record)

    payload = {field: _stringify_value(record.get(field)) for field in selected_fields if field in record}
    if not payload:
        return dict(record)

    messages = [
        {
            "role": "system",
            "content": "Translate only the provided user-facing fields. Preserve non-text fields exactly. Return valid JSON only.",
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "target_language": target_language,
                    "fields": payload,
                },
                ensure_ascii=False,
                separators=(",", ":"),
            ),
        },
    ]

    response = _client().chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    translated = json.loads(content)
    if not isinstance(translated, dict):
        raise ValueError("translation response must be a JSON object")

    output = dict(record)
    for field in selected_fields:
        if field in translated:
            output[field] = translated[field]
    return output
