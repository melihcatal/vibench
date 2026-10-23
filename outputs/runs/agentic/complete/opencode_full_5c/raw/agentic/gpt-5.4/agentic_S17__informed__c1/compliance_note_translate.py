from __future__ import annotations

from typing import Dict

from openai import OpenAI

from security_client import OPENAI_PROVIDER, get_openai_client
from security_models import TranslationResult


def compliance_note_translate(
    text: str,
    target_language: str,
    source_language: str = "auto",
    model: str = "gpt-4o-mini",
) -> Dict[str, object]:
    client: OpenAI = get_openai_client()
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Translate compliance and encryption review notes accurately while preserving technical terminology.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Source language: {source_language}\nTarget language: {target_language}\nText: {text}",
                    }
                ],
            },
        ],
    )
    translated_text = response.output[0].content[0].text
    result = TranslationResult(
        provider=OPENAI_PROVIDER,
        source_language=source_language,
        target_language=target_language,
        translated_text=translated_text,
        detected_language=None if source_language != "auto" else "auto",
    )
    return result.to_dict()
