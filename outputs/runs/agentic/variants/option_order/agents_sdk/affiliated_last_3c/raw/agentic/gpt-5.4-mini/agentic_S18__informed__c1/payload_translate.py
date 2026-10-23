from __future__ import annotations

from openai import OpenAI

from messaging_models import normalize_text


MODEL = "gpt-4o-mini"


def translate_payload_text(text: str, target_language: str = "es") -> dict:
    client = OpenAI()
    source_text = normalize_text(text)
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You translate customer-facing messaging content accurately and naturally."},
            {"role": "user", "content": f"Translate this text to {target_language}: {source_text}"},
        ],
    )
    return {
        "provider": "openai",
        "model": MODEL,
        "target_language": target_language,
        "source_text": source_text,
        "translated_text": completion.choices[0].message.content,
    }
