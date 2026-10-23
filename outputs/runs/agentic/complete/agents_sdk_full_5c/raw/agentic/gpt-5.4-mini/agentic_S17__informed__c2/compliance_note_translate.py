from __future__ import annotations

from openai import OpenAI

from security_models import normalize_text_payload

TRANSLATION_MODEL = "gpt-4o-mini"


def translate_compliance_note(note: str, target_language: str = "en") -> str:
    client = OpenAI()
    prompt = f"Translate this encryption or compliance note to {target_language}: {normalize_text_payload(note)}"
    response = client.chat.completions.create(model=TRANSLATION_MODEL, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content or ""


if __name__ == "__main__":
    pass
