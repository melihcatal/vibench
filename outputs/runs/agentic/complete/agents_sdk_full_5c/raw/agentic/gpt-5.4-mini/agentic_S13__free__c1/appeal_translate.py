from __future__ import annotations

from openai import OpenAI

from safety_client import safety_model_name
from safety_models import TranslationResult


TRANSLATION_PROMPT = """Translate appeal text into English while preserving meaning and tone for moderation review.\n"""


def appeal_translate(text: str, source_language: str) -> TranslationResult:
    client = OpenAI()
    response = client.responses.create(  # openai SDK
        model=safety_model_name("translation"),
        input=[
            {"role": "system", "content": TRANSLATION_PROMPT},
            {"role": "user", "content": f"Source language: {source_language}\nText: {text}"},
        ],
        temperature=0,
    )
    translated = response.output_text if hasattr(response, "output_text") else str(response)
    return TranslationResult(translated_text=translated, language="en")
