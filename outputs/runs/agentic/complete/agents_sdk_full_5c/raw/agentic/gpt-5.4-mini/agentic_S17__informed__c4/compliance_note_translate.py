from __future__ import annotations

from openai import OpenAI

from security_models import TranslationResult, normalize_text


TRANSLATION_MODEL = "gpt-4.1-mini"


def compliance_note_translate(note: str, target_language: str = "es") -> TranslationResult:
    client = OpenAI()
    prompt = f"Translate this encryption/compliance note into {target_language}: {normalize_text(note)}"
    response = client.responses.create(model=TRANSLATION_MODEL, input=prompt)
    translated_text = response.output_text
    return TranslationResult(source_text=normalize_text(note), translated_text=translated_text, source_language="en", target_language=target_language)
