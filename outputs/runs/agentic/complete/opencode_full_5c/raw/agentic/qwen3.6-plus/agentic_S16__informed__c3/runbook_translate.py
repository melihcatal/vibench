import os
from typing import List, Optional
import deepl

from security_models import RunbookEntry


def translate_runbook(
    entries: Optional[List[RunbookEntry]] = None,
    target_lang: Optional[str] = None,
) -> dict:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    if entries is None:
        entries = []
    if target_lang is None:
        target_lang = os.environ.get("TRANSLATION_TARGET_LANG", "JA")

    translator = deepl.Translator(auth_key)

    translated_entries = []

    for entry in entries:
        title_result = translator.translate_text(
            entry.title,
            source_lang=entry.source_language.upper()
            if len(entry.source_language) == 2
            else None,
            target_lang=target_lang.upper(),
        )

        content_result = translator.translate_text(
            entry.content,
            source_lang=entry.source_language.upper()
            if len(entry.source_language) == 2
            else None,
            target_lang=target_lang.upper(),
        )

        translated_entries.append(
            {
                "entry_id": entry.entry_id,
                "original_title": entry.title,
                "translated_title": title_result.text,
                "original_content": entry.content,
                "translated_content": content_result.text,
                "source_language": entry.source_language,
                "target_language": target_lang.lower(),
            }
        )

    return {
        "translated_entries": translated_entries,
        "provider": "deepl",
        "model": "deepl-translate",
    }


def translate_single_runbook(
    entry: RunbookEntry, target_lang: Optional[str] = None
) -> dict:
    return translate_runbook(entries=[entry], target_lang=target_lang)


if __name__ == "__main__":
    test_entries = [
        RunbookEntry(
            entry_id="rb-001",
            title="Rotate API Key for Production Service",
            content=(
                "Step 1: Generate a new API key in AWS Secrets Manager.\n"
                "Step 2: Update the application configuration to use the new key.\n"
                "Step 3: Verify the application can authenticate with the new key.\n"
                "Step 4: Mark the old key version as deprecated.\n"
                "Step 5: Remove the old key version after 24 hours."
            ),
            source_language="en",
            target_language="ja",
        ),
    ]
    result = translate_runbook(entries=test_entries)
    import json

    print(json.dumps(result, indent=2))
