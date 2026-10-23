import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini")


def translate_consent_copy(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
) -> str:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    messages: List[Dict[str, Any]] = [
        {
            "role": "system",
            "content": "You translate identity-provider consent copy accurately, preserving meaning, tone, and any placeholders or markup.",
        },
        {
            "role": "user",
            "content": _build_prompt(text, target_language, source_language),
        },
    ]
    response = client.responses.create(model=OPENAI_MODEL, input=messages)
    return _extract_text(response)


def _build_prompt(text: str, target_language: str, source_language: Optional[str]) -> str:
    parts = [f"Translate the following consent copy into {target_language}."]
    if source_language:
        parts.append(f"The source language is {source_language}.")
    parts.append("Return only the translated text.")
    parts.append(text)
    return "\n\n".join(parts)


def _extract_text(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if output_text:
        return output_text.strip()
    output = getattr(response, "output", [])
    chunks: List[str] = []
    for item in output:
        content = getattr(item, "content", None) or []
        for part in content:
            text = getattr(part, "text", None)
            if text:
                chunks.append(text)
    return "".join(chunks).strip()
