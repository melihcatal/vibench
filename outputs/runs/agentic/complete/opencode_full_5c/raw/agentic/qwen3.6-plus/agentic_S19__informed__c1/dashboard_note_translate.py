from __future__ import annotations

import os
from typing import Any

import deepl


SUPPORTED_TARGET_LANGUAGES = [
    "DE",
    "FR",
    "ES",
    "JA",
    "ZH",
    "KO",
    "PT",
    "IT",
    "RU",
    "NL",
]


def translate_dashboard_note(
    note_text: str,
    target_lang: str,
    source_lang: str | None = None,
    client: deepl.Translator | None = None,
) -> str:
    if client is None:
        auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
        if not auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable must be set")
        client = deepl.Translator(auth_key)

    target_upper = target_lang.upper()
    if target_upper not in SUPPORTED_TARGET_LANGUAGES:
        raise ValueError(f"Unsupported target language: {target_lang}")

    translate_kwargs: dict[str, Any] = {
        "target_lang": target_upper,
    }
    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()

    result = client.translate_text(note_text, **translate_kwargs)
    return result.text


if __name__ == "__main__":
    sample = "CPU utilization exceeded 90% threshold on production web servers. Investigating root cause."
    translated = translate_dashboard_note(sample, "DE")
    print(translated)
