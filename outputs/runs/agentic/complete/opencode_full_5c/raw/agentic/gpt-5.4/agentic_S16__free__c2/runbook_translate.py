from __future__ import annotations

import os

from deepl import DeepLClient


def runbook_translate(
    runbook_notes: str, target_lang: str, source_lang: str | None = None
) -> dict:
    client = DeepLClient(os.environ["DEEPL_AUTH_KEY"])
    result = client.translate_text(
        runbook_notes, target_lang=target_lang, source_lang=source_lang
    )
    return {
        "provider": "deepl",
        "target_lang": target_lang,
        "source_lang": result.detected_source_lang,
        "text": result.text,
    }
