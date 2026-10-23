import os
from typing import List, Dict
from observability_client import get_log_client


def translate_log_messages(
    log_entries: List[Dict[str, Any]], target_locale: str = "es"
) -> List[Dict[str, Any]]:
    """Translate human‑readable log messages to another language for support teams.

    Leverages a machine‑translation provider such as Amazon Translate, Google Cloud Translation,
    Alibaba Cloud MT, or Azure Translator. The function adds a new field `translated_message`
    to each log entry and retains the original `message` for reference. The caller can filter
    on `translated_message` when presenting logs to non‑English audiences.
    """
    client = get_log_client()
    if os.getenv("TRANSLATION_PROVIDER", "amazon_translate") == "amazon_translate":
        import boto3

        translate = boto3.client(service_name="translate")
        translated_entries = []
        for entry in log_entries:
            orig = entry.get("message", "")
            if not orig:
                entry["translated_message"] = orig
                translated_entries.append(entry)
                continue
            response = translate.translate_text(
                Text=orig, SourceLanguageCode="en", TargetLanguageCode=target_locale
            )
            entry["translated_message"] = response.get("TranslatedText", orig)
            translated_entries.append(entry)
    # Add placeholders for other providers (Google, Alibaba, Azure, DeepL)
    return translated_entries
