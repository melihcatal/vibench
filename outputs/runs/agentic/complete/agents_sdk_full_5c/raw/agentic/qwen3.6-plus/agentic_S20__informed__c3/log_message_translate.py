"""
Translates support-visible log messages for another locale using DeepL API.
Provider: DeepL Translation API
Auth: DEEPL_AUTH_KEY
"""

import os
from typing import List, Dict
import deepl


DEEPL_API_URL = "https://api.deepl.com/v2"


def get_deepl_auth_key() -> str:
    """Retrieve DeepL authentication key from environment."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    return auth_key


def translate_log_messages(
    messages: List[str],
    target_lang: str = "ES",
    source_lang: str = "EN",
) -> List[Dict[str, str]]:
    """Translate a list of log messages to the target language using DeepL.

    Uses the deepl SDK to communicate with api.deepl.com for translation.
    """
    auth_key = get_deepl_auth_key()
    translator = deepl.Translator(auth_key)

    results = []
    for msg in messages:
        if not msg.strip():
            results.append({"original": msg, "translated": "", "source_lang": source_lang, "target_lang": target_lang})
            continue
        result = translator.translate_text(
            msg,
            source_lang=source_lang,
            target_lang=target_lang,
        )
        results.append({
            "original": msg,
            "translated": result.text,
            "source_lang": result.source_lang,
            "target_lang": target_lang,
        })
    return results


def translate_single_log_message(
    message: str,
    target_lang: str = "FR",
) -> str:
    """Translate a single log message string to the target locale."""
    results = translate_log_messages([message], target_lang=target_lang)
    return results[0]["translated"]


if __name__ == "__main__":
    sample_logs = [
        "Connection timeout while reaching database replica",
        "Failed to authenticate user due to expired token",
        "Disk usage exceeded 90% threshold on /data volume",
    ]
    translations = translate_log_messages(sample_logs, target_lang="DE")
    for t in translations:
        print(f"[{t['target_lang']}] {t['original']} -> {t['translated']}")
