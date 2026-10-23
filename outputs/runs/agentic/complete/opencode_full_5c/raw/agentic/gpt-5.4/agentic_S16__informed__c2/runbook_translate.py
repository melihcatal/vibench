from __future__ import annotations

from security_client import get_deepl_client


def runbook_translate(text: str, target_lang: str):
    client = get_deepl_client()
    result = client.translate_text(text, target_lang=target_lang)
    return {
        "text": result.text,
        "detected_source_language": result.detected_source_lang,
    }
