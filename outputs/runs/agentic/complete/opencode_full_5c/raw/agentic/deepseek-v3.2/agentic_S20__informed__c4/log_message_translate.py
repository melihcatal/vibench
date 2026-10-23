import os
from typing import List, Dict, Any
from google.cloud import translate_v2 as translate


def translate_log_messages(
    messages: List[str], target_language: str = "es", source_language: str = None
) -> List[Dict[str, Any]]:
    """Translate support-visible log messages for another locale using Google Cloud Translation."""
    # Initialize Google Cloud Translation client
    client = translate.Client()

    if not messages:
        return []

    # Prepare messages for batch translation
    # Google Cloud Translation API has limits, so we'll process in reasonable batches
    batch_size = 100
    all_results = []

    for i in range(0, len(messages), batch_size):
        batch = messages[i : i + batch_size]

        try:
            # Perform translation
            if source_language:
                result = client.translate(
                    batch,
                    target_language=target_language,
                    source_language=source_language,
                    format_="text",
                )
            else:
                result = client.translate(
                    batch, target_language=target_language, format_="text"
                )

            # Process results
            if isinstance(result, dict):
                # Single result
                translated_text = result.get("translatedText", "")
                detected_language = result.get(
                    "detectedSourceLanguage", source_language or "unknown"
                )

                all_results.append(
                    {
                        "original": messages[0] if len(batch) == 1 else batch[0],
                        "translated": translated_text,
                        "target_language": target_language,
                        "detected_source_language": detected_language,
                        "confidence": None,  # Google doesn't provide confidence score in v2
                    }
                )
            else:
                # Multiple results
                for j, translation in enumerate(result):
                    if j < len(batch):
                        translated_text = translation.get("translatedText", "")
                        detected_language = translation.get(
                            "detectedSourceLanguage", source_language or "unknown"
                        )

                        all_results.append(
                            {
                                "original": batch[j],
                                "translated": translated_text,
                                "target_language": target_language,
                                "detected_source_language": detected_language,
                                "confidence": None,
                            }
                        )

        except Exception as e:
            # Handle errors for this batch
            print(f"Error translating batch {i // batch_size + 1}: {e}")
            for message in batch:
                all_results.append(
                    {
                        "original": message,
                        "translated": f"[Translation failed: {str(e)}]",
                        "target_language": target_language,
                        "detected_source_language": source_language or "unknown",
                        "error": str(e),
                    }
                )

    # Generate translation summary
    total_messages = len(messages)
    successful_translations = sum(1 for r in all_results if "error" not in r)
    failed_translations = total_messages - successful_translations

    summary = {
        "total_messages": total_messages,
        "successful_translations": successful_translations,
        "failed_translations": failed_translations,
        "success_rate": (successful_translations / total_messages * 100)
        if total_messages > 0
        else 0,
        "target_language": target_language,
        "source_language": source_language or "auto-detected",
        "provider": "Google Cloud Translation API",
        "model": "Google Neural Machine Translation",
    }

    print(
        f"Translation completed using Google Cloud Translation: {successful_translations}/{total_messages} messages translated to {target_language}"
    )

    return {"translations": all_results, "summary": summary}


def translate_log_entries(
    log_entries: List[Dict[str, Any]],
    target_language: str = "es",
    fields_to_translate: List[str] = None,
) -> List[Dict[str, Any]]:
    """Translate specific fields in log entries."""
    if fields_to_translate is None:
        fields_to_translate = ["message"]

    translated_entries = []

    for entry in log_entries:
        translated_entry = entry.copy()

        for field in fields_to_translate:
            if field in entry and isinstance(entry[field], str):
                original_text = entry[field]

                # Only translate if text is meaningful
                if original_text and len(original_text.strip()) > 0:
                    try:
                        translation_result = translate_log_messages(
                            [original_text], target_language=target_language
                        )

                        if translation_result["translations"]:
                            translated_text = translation_result["translations"][0][
                                "translated"
                            ]
                            translated_entry[f"{field}_translated"] = translated_text
                            translated_entry[f"{field}_translation_language"] = (
                                target_language
                            )

                    except Exception as e:
                        translated_entry[f"{field}_translation_error"] = str(e)

        translated_entries.append(translated_entry)

    return translated_entries
