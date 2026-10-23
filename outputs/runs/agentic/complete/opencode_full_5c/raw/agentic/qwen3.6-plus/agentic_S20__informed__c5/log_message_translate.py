import os
import sys
import json
from typing import Optional

import deepl

from observability_models import LogEntry


def translate_log_message(
    text: str,
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
) -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError(
            "DEEPL_AUTH_KEY environment variable is required for DeepL API"
        )

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
    )
    return result.text


def translate_log_entries(
    entries: list[LogEntry],
    target_lang: str = "ES",
    source_lang: Optional[str] = None,
) -> list[dict]:
    translated = []
    for entry in entries:
        if not entry.message.strip():
            continue
        translated_text = translate_log_message(
            entry.message,
            target_lang=target_lang,
            source_lang=source_lang,
        )
        translated.append(
            {
                "log_id": entry.id,
                "timestamp": entry.timestamp,
                "service": entry.service,
                "severity": entry.severity,
                "original_message": entry.message,
                "translated_message": translated_text,
                "target_language": target_lang,
            }
        )
    return translated


def main():
    log_file = sys.argv[1] if len(sys.argv) > 1 else ""
    target_lang = sys.argv[2] if len(sys.argv) > 2 else "ES"
    source_lang = sys.argv[3] if len(sys.argv) > 3 else None

    if log_file:
        with open(log_file, "r") as f:
            data = json.load(f)
        entries = [LogEntry(**e) for e in data.get("entries", [])]
    else:
        entries = [
            LogEntry(
                id="log-1",
                timestamp="2026-04-21T10:00:00Z",
                message="Connection pool exhausted, unable to acquire database connection",
                severity="error",
                service="api-gateway",
            ),
            LogEntry(
                id="log-2",
                timestamp="2026-04-21T10:01:00Z",
                message="Payment processing timeout after 30 seconds",
                severity="critical",
                service="payment-service",
            ),
        ]

    translations = translate_log_entries(
        entries, target_lang=target_lang, source_lang=source_lang
    )
    print(json.dumps(translations, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
