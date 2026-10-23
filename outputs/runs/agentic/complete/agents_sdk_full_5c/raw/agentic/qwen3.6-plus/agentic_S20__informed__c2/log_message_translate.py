"""
log_message_translate.py

Translate support-visible log messages for another locale using the
DeepL API via the deepl SDK.

Required env: DEEPL_AUTH_KEY
"""

import os
from typing import List, Dict, Optional
import deepl
from observability_models import QueryResponse, LogQueryResult


def translate_log_messages(
    log_results: QueryResponse,
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
) -> List[Dict[str, str]]:
    """
    Translate log messages to a target locale using the DeepL API.

    Args:
        log_results: QueryResponse containing log entries with messages.
        target_lang: ISO target language code (e.g. 'ES', 'FR', 'DE', 'JA').
        source_lang: Source language code (auto-detected if None).

    Returns:
        List of dicts with original and translated message text.
    """
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(auth_key)

    messages = [r.message for r in log_results.results if r.message and len(r.message) > 0]
    # Deduplicate
    seen = set()
    unique_messages = []
    for m in messages:
        if m not in seen:
            seen.add(m)
            unique_messages.append(m)

    results = []
    for msg in unique_messages:
        translated = translator.translate_text(
            msg,
            source_lang=source_lang,
            target_lang=target_lang,
        )
        results.append({
            "original": msg,
            "translated": translated.text,
            "target_language": target_lang,
        })

    return results


if __name__ == "__main__":
    from query_error_logs import query_error_logs

    lg = os.environ.get("CLOUDWATCH_LOG_GROUP", "/app/production")
    errors = query_error_logs(
        log_group_name=lg,
        hours_back=2,
        log_level_filter="ERROR",
        limit=20,
    )
    translations = translate_log_messages(errors, target_lang="ES")
    for t in translations[:5]:
        print(f"  [{t['target_language']}] {t['translated']}")
