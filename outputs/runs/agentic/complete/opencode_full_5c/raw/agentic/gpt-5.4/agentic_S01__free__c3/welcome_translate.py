from __future__ import annotations

from identity_client import openai_post
from identity_models import TranslationRequest


def welcome_translate(request: TranslationRequest):
    payload = {
        "model": "gpt-4.1-mini",
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Translate onboarding copy accurately while preserving friendly tone.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Source locale: {request.source_locale or 'auto'}\nTarget locale: {request.target_locale}\nText: {request.text}",
                    }
                ],
            },
        ],
    }
    response = openai_post(payload)
    return {
        "provider": "openai",
        "model": "gpt-4.1-mini",
        "target_locale": request.target_locale,
        "translation": response.get("output", []),
        "raw": response,
    }
