import os
from typing import Any, Dict, List

from openai import OpenAI


def translate_payload_text(text: str, target_language: str, source_language: str = "auto") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": "Translate customer-facing message payload text faithfully and preserve meaning, names, numbers, punctuation, and formatting.",
            },
            {
                "role": "user",
                "content": f"Source language: {source_language}\nTarget language: {target_language}\nText: {text}",
            },
        ],
    )
    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text.strip()
    chunks: List[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            chunk = getattr(content, "text", None)
            if chunk:
                chunks.append(chunk)
    return "".join(chunks).strip()


def translate_payload(payload: Dict[str, Any], target_language: str, source_language: str = "auto") -> Dict[str, Any]:
    translated = dict(payload)
    for key in ("text", "message", "body", "content"):
        value = translated.get(key)
        if isinstance(value, str) and value.strip():
            translated[key] = translate_payload_text(value, target_language, source_language)
            break
    return translated
