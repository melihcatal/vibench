from __future__ import annotations

import os

from openai import OpenAI

from security_models import TranslatedRunbook


_PROVIDER = "openai"
_MODEL = "gpt-4o-mini"


def runbook_translate(source_text: str, target_language: str) -> TranslatedRunbook:
    client = OpenAI()
    response = client.responses.create(
        model=_MODEL,
        input=f"Translate the following secret-rotation runbook into {target_language}:\n{source_text}",
    )
    translated = response.output_text
    return TranslatedRunbook(provider=_PROVIDER, source_text=source_text, target_language=target_language, translated_text=translated)


if __name__ == "__main__":
    source_text = os.environ.get("RUNBOOK_TEXT", "Rotate the secret and verify dependent services.")
    target_language = os.environ.get("TARGET_LANGUAGE", "Spanish")
    result = runbook_translate(source_text, target_language)
    print(result.translated_text)
