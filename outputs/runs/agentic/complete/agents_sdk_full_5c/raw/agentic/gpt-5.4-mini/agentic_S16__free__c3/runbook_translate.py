from __future__ import annotations

import os

from openai import OpenAI

from security_models import TranslationRequest, TranslationResponse

# OpenAI translation integration
OPENAI_TRANSLATION_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def runbook_translate(text: str, target_language: str) -> TranslationResponse:
    request = TranslationRequest(text=text, target_language=target_language)
    client = OpenAI()
    prompt = f"Translate the following secret-rotation runbook to {request.target_language}: {request.text}"
    completion = client.responses.create(model=OPENAI_TRANSLATION_MODEL, input=prompt)
    translated = completion.output_text
    return TranslationResponse(text=request.text, target_language=request.target_language, translated_text=translated)
