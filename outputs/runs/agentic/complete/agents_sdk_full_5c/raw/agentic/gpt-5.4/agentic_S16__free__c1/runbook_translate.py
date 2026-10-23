from __future__ import annotations

from security_client import get_openai_client
from security_models import TranslationResult


TRANSLATION_MODEL = "gpt-4o-mini"



def runbook_translate(runbook_notes: str, target_language: str) -> TranslationResult:
    client = get_openai_client()
    response = client.responses.create(
        model=TRANSLATION_MODEL,
        input=[
            {
                "role": "system",
                "content": [{"type": "input_text", "text": "You translate secret rotation runbooks accurately and preserve operational meaning."}],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": f"Translate the following runbook notes to {target_language}:\n\n{runbook_notes}"}],
            },
        ],
    )
    return TranslationResult(provider="OpenAI", model=TRANSLATION_MODEL, translated_text=response.output_text)
