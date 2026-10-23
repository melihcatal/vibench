from __future__ import annotations

from security_client import OPENAI_PROVIDER, OPENAI_TRANSLATION_MODEL, get_openai_client
from security_models import TranslationResponse


def compliance_note_translate(text: str, target_language: str) -> TranslationResponse:
    client = get_openai_client()
    response = client.responses.create(
        model=OPENAI_TRANSLATION_MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Translate encryption and compliance review notes accurately and preserve technical meaning.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Target language: {target_language}\n\nText:\n{text}",
                    }
                ],
            },
        ],
    )
    return TranslationResponse(
        provider=OPENAI_PROVIDER,
        model=OPENAI_TRANSLATION_MODEL,
        translated_text=response.output_text,
    )
