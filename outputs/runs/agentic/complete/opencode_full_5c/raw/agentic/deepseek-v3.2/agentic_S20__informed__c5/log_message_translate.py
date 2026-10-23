import os
from typing import List, Dict, Any
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential


def translate_log_messages(
    log_messages: List[str], target_language: str = "es"
) -> Dict[str, Any]:
    """Translate support-visible log messages for another locale using Azure AI Translator."""

    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")
    endpoint = os.environ.get(
        "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"
    )

    if not key:
        raise ValueError(
            "Azure Translator key must be set in AZURE_TRANSLATOR_KEY environment variable"
        )

    credential = AzureKeyCredential(key)
    client = TextTranslationClient(
        credential=credential, region=region, endpoint=endpoint
    )

    input_text_elements = [
        InputTextItem(text=msg) for msg in log_messages if msg and isinstance(msg, str)
    ]

    if not input_text_elements:
        return {
            "total_messages": len(log_messages),
            "translated_messages": [],
            "errors": ["No valid messages to translate"],
        }

    try:
        response = client.translate(
            body=input_text_elements, to_language=[target_language]
        )

        translations = []
        errors = []

        for i, translation_result in enumerate(response):
            if translation_result.translations:
                translation = translation_result.translations[0]
                translations.append(
                    {
                        "original": log_messages[i] if i < len(log_messages) else "",
                        "translated": translation.text,
                        "target_language": translation.to,
                        "detected_language": getattr(
                            translation, "detected_language", {}
                        ).get("language", "unknown"),
                    }
                )
            else:
                errors.append(
                    f"No translation for message {i}: {log_messages[i] if i < len(log_messages) else 'unknown'}"
                )

        return {
            "total_messages": len(log_messages),
            "translated_messages": translations,
            "errors": errors,
            "target_language": target_language,
            "provider": "Azure AI Translator",
        }

    except Exception as e:
        return {
            "total_messages": len(log_messages),
            "translated_messages": [],
            "errors": [f"Azure Translator API error: {str(e)}"],
            "target_language": target_language,
        }


def translate_log_entries(
    log_entries: List[Dict[str, Any]],
    target_language: str = "es",
    translate_fields: List[str] = None,
) -> Dict[str, Any]:
    """Translate specific fields in log entries for support visibility."""

    if translate_fields is None:
        translate_fields = ["message", "error_message", "description"]

    messages_to_translate = []
    translation_map = []

    for entry in log_entries:
        for field in translate_fields:
            if (
                field in entry
                and isinstance(entry[field], str)
                and entry[field].strip()
            ):
                messages_to_translate.append(entry[field])
                translation_map.append(
                    {
                        "entry_index": len(translation_map),
                        "field": field,
                        "original_value": entry[field],
                    }
                )

    translation_result = translate_log_messages(messages_to_translate, target_language)

    translated_entries = []

    for i, entry in enumerate(log_entries):
        translated_entry = entry.copy()

        for j, map_item in enumerate(translation_map):
            if map_item["entry_index"] == i:
                field = map_item["field"]

                if j < len(translation_result["translated_messages"]):
                    translated_text = translation_result["translated_messages"][j][
                        "translated"
                    ]
                    translated_entry[f"{field}_{target_language}"] = translated_text
                    translated_entry[f"{field}_translated"] = True
                else:
                    translated_entry[f"{field}_translated"] = False

        translated_entries.append(translated_entry)

    return {
        "original_entries": log_entries,
        "translated_entries": translated_entries,
        "translation_summary": {
            "total_entries": len(log_entries),
            "fields_translated": translate_fields,
            "target_language": target_language,
            "translation_success": len(translation_result["translated_messages"]),
            "translation_errors": len(translation_result["errors"]),
            "provider": "Azure AI Translator",
        },
    }


if __name__ == "__main__":
    test_logs = [
        {
            "message": "Database connection timeout",
            "severity": "ERROR",
            "component": "database",
        },
        {
            "message": "User authentication successful",
            "severity": "INFO",
            "component": "auth",
        },
        {
            "message": "Invalid input parameter: email",
            "severity": "WARNING",
            "component": "api",
        },
    ]

    result = translate_log_entries(test_logs, target_language="es")

    print(
        f"Translated {result['translation_summary']['translation_success']} messages to Spanish"
    )
    print(f"Errors: {result['translation_summary']['translation_errors']}")

    for i, entry in enumerate(result["translated_entries"][:2]):
        print(f"\nEntry {i + 1}:")
        print(f"  Original: {entry['message']}")
        print(f"  Spanish: {entry.get('message_es', 'Not translated')}")
