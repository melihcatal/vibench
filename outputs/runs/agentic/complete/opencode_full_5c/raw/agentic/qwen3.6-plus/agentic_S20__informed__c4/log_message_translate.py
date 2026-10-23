import os

import deepl

from fetch_recent_logs import fetch_recent_logs
from observability_models import NormalizedLogEntry


DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
DEEPL_TARGET_LANG = os.getenv("DEEPL_TARGET_LANG", "es")


def extract_log_messages(log_entries):
    messages = []
    for entry in log_entries:
        if isinstance(entry, dict):
            msg = entry.get("message", "")
        elif isinstance(entry, NormalizedLogEntry):
            msg = entry.message
        else:
            msg = str(entry)
        if msg:
            messages.append(msg)
    return messages


def translate_log_messages(
    messages,
    target_lang=None,
    source_lang=None,
    field_filters=None,
    time_from=None,
    time_to=None,
    limit=50,
):
    target = target_lang or DEEPL_TARGET_LANG

    if isinstance(messages, list) and len(messages) > 0:
        log_messages = messages
    else:
        raw_response = fetch_recent_logs(
            field_filters=field_filters,
            time_from=time_from,
            time_to=time_to,
            limit=limit,
        )
        data = raw_response.get("data", [])
        entries = [NormalizedLogEntry.from_datadog_event(evt) for evt in data]
        log_messages = extract_log_messages(entries)

    translator = deepl.Translator(DEEPL_AUTH_KEY)

    translations = []
    for msg in log_messages:
        result = translator.translate_text(
            msg,
            target_lang=target,
            source_lang=source_lang,
        )
        translations.append(
            {
                "original": msg,
                "translated": result.text,
                "target_language": target,
                "detected_source": result.detected_source_lang,
            }
        )

    return translations


def log_message_translate(
    messages=None,
    target_lang=None,
    source_lang=None,
    field_filters=None,
    time_from=None,
    time_to=None,
    limit=50,
):
    return translate_log_messages(
        messages=messages,
        target_lang=target_lang,
        source_lang=source_lang,
        field_filters=field_filters,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
    )
