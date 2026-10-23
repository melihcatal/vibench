"""
Translates support-visible log messages for another locale.

Uses the Google Cloud Translation API (translation.googleapis.com)
via the google-cloud-translate SDK to translate log messages.
Auth: GOOGLE_APPLICATION_CREDENTIALS environment variable.
"""

import json
import os
from typing import Optional

from google.cloud import translate_v2 as translate


def translate_log_messages(
    messages: list[dict],
    target_language: str = "en",
    source_language: Optional[str] = None,
    format_type: str = "text",
) -> list[dict]:
    """Translate log messages using the Google Cloud Translation API.

    Uses the google-cloud-translate SDK (google.cloud.translate_v2)
    which connects to translation.googleapis.com. Each log message's
    'message' field is translated to the target language.
    """
    client = translate.Client()

    texts_to_translate = [entry.get("message", "") for entry in messages]

    kwargs: dict = {
        "target_language": target_language,
        "format_": format_type,
    }
    if source_language:
        kwargs["source_language"] = source_language

    results = client.translate(texts_to_translate, **kwargs)

    # Normalize results into a list of translation dicts
    if isinstance(results, dict):
        # Single translation result
        translated_results = [results]
    else:
        translated_results = results

    output = []
    for idx, entry in enumerate(messages):
        original = entry.copy()
        translation_data = translated_results[idx] if idx < len(translated_results) else {}
        translated_text = translation_data.get("translatedText", original["message"])
        detected_source = translation_data.get("detectedSourceLanguage", source_language or "unknown")

        output.append({
            "original": original,
            "translated_message": translated_text,
            "target_language": target_language,
            "detected_source_language": detected_source,
            "translation_model": "nmt",
        })

    return output


def format_translation_report(translated_entries: list[dict]) -> str:
    """Format a human-readable translation report."""
    lines = [
        "Log Message Translation Report (Google Cloud Translation API)",
        "=" * 60,
        f"Messages translated: {len(translated_entries)}",
        "",
    ]

    for i, entry in enumerate(translated_entries, 1):
        original = entry.get("original", {})
        lines.append(f"[{i}] Service: {original.get('service', 'unknown')}")
        lines.append(f"    Original ({entry.get('detected_source_language', 'unknown')}):")
        lines.append(f"      {original.get('message', '')}")
        lines.append(f"    Translated ({entry.get('target_language', 'en')}):")
        lines.append(f"      {entry.get('translated_message', '')}")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    """Entry point for translating log messages."""
    sample_messages = [
        {
            "message": "El servicio de autenticación no pudo verificar las credenciales del usuario",
            "timestamp": "2025-01-15T10:00:00Z",
            "service": "auth-service",
            "status": "error",
        },
        {
            "message": "Die Datenbankverbindung wurde nach 30 Sekunden abgebrochen",
            "timestamp": "2025-01-15T10:05:00Z",
            "service": "database-service",
            "status": "error",
        },
        {
            "message": "Le traitement de la requête a échoué avec le code d'erreur 500",
            "timestamp": "2025-01-15T10:10:00Z",
            "service": "api-processor",
            "status": "error",
        },
    ]

    target_lang = os.environ.get("TRANSLATION_TARGET_LANGUAGE", "en")

    translated = translate_log_messages(sample_messages, target_language=target_lang)

    report = format_translation_report(translated)
    print(report)

    print("\n--- Raw JSON ---")
    print(json.dumps(translated, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
