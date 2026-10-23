import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def translate_text(text: str, source_language: str, target_language: str, glossary: Optional[Dict[str, str]] = None) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not text:
        return ""
    if not source_language or not target_language:
        raise ValueError("source_language and target_language are required")

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")

    glossary_lines = ""
    if glossary:
        glossary_lines = "\n".join(f"{k} => {v}" for k, v in glossary.items())

    prompt = (
        f"Translate the following text from {source_language} to {target_language}. "
        f"Preserve meaning, tone, numbers, and formatting. Return only the translated text."
    )
    if glossary_lines:
        prompt += f"\nUse this glossary when appropriate:\n{glossary_lines}"

    response = requests.post(
        f"{OPENAI_API_BASE.rstrip('/')}/responses",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_TRANSLATION_MODEL,
            "input": [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": "You are a professional translation engine."}],
                },
                {
                    "role": "user",
                    "content": [{"type": "text", "text": f"{prompt}\n\n{text}"}],
                },
            ],
        },
        timeout=60,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()

    output = data.get("output", [])
    for item in output:
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text" and content.get("text"):
                    return content["text"].strip()

    raise RuntimeError("No translation returned by OpenAI Responses API")
