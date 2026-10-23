import os
import json
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError


def translate_log_message(
    text: str, source_language_code: str = "auto", target_language_code: str = "en"
) -> Dict[str, Any]:
    """Translate support-visible log messages for another locale using Amazon Translate."""

    # AWS credentials from environment
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    try:
        # Initialize Amazon Translate client
        translate_client = boto3.client(
            "translate",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )

        # Call Amazon Translate
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )

        # Extract translation result
        translated_text = response["TranslatedText"]
        detected_source_language = response.get(
            "SourceLanguageCode", source_language_code
        )

        return {
            "translation": {
                "original_text": text,
                "translated_text": translated_text,
                "source_language": detected_source_language,
                "target_language": target_language_code,
                "character_count": len(text),
                "translated_character_count": len(translated_text),
            },
            "metadata": {
                "service": "Amazon Translate",
                "region": aws_region,
                "model": "Amazon Translate neural machine translation",
            },
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        return {
            "translation": {
                "original_text": text,
                "translated_text": None,
                "source_language": source_language_code,
                "target_language": target_language_code,
                "error": error_message,
                "error_code": error_code,
            },
            "metadata": {
                "service": "Amazon Translate",
                "region": aws_region,
                "error": True,
            },
        }
    except Exception as e:
        return {
            "translation": {
                "original_text": text,
                "translated_text": None,
                "source_language": source_language_code,
                "target_language": target_language_code,
                "error": str(e),
            },
            "metadata": {
                "service": "Amazon Translate",
                "region": aws_region,
                "error": True,
            },
        }


def translate_logs_batch(
    log_entries: List[Dict[str, Any]],
    target_language_code: str = "en",
    fields_to_translate: List[str] = None,
) -> Dict[str, Any]:
    """Translate multiple log entries in batch."""

    if fields_to_translate is None:
        fields_to_translate = ["message", "error_message", "description"]

    results = []
    successful_translations = 0
    failed_translations = 0

    for i, log_entry in enumerate(log_entries):
        entry_result = {
            "index": i,
            "log_id": log_entry.get("id", f"log_{i}"),
            "timestamp": log_entry.get("timestamp"),
            "severity": log_entry.get("severity"),
            "translations": {},
        }

        # Translate specified fields
        for field in fields_to_translate:
            if field in log_entry and log_entry[field]:
                text_to_translate = str(log_entry[field])

                # Skip very short or empty text
                if len(text_to_translate.strip()) < 3:
                    entry_result["translations"][field] = {
                        "original": text_to_translate,
                        "translated": text_to_translate,
                        "skipped": "too_short",
                    }
                    continue

                try:
                    translation_result = translate_log_message(
                        text_to_translate,
                        source_language_code="auto",
                        target_language_code=target_language_code,
                    )

                    if translation_result["translation"].get("translated_text"):
                        entry_result["translations"][field] = {
                            "original": text_to_translate,
                            "translated": translation_result["translation"][
                                "translated_text"
                            ],
                            "source_language": translation_result["translation"].get(
                                "source_language"
                            ),
                            "success": True,
                        }
                        successful_translations += 1
                    else:
                        entry_result["translations"][field] = {
                            "original": text_to_translate,
                            "translated": None,
                            "error": translation_result["translation"].get("error"),
                            "success": False,
                        }
                        failed_translations += 1

                except Exception as e:
                    entry_result["translations"][field] = {
                        "original": text_to_translate,
                        "translated": None,
                        "error": str(e),
                        "success": False,
                    }
                    failed_translations += 1

        results.append(entry_result)

    # Create translated log entries
    translated_logs = []
    for result in results:
        translated_log = {}
        for key, value in result.items():
            if key != "translations":
                translated_log[key] = value

        # Add translated fields
        for field, translation in result.get("translations", {}).items():
            if translation.get("success") and translation.get("translated"):
                translated_log[f"{field}_translated"] = translation["translated"]
                translated_log[f"{field}_original_language"] = translation.get(
                    "source_language", "unknown"
                )

        translated_logs.append(translated_log)

    return {
        "summary": {
            "total_logs": len(log_entries),
            "successful_translations": successful_translations,
            "failed_translations": failed_translations,
            "success_rate": (
                successful_translations
                / (successful_translations + failed_translations)
                * 100
            )
            if (successful_translations + failed_translations) > 0
            else 0,
            "target_language": target_language_code,
            "fields_translated": fields_to_translate,
        },
        "detailed_results": results,
        "translated_logs": translated_logs,
    }


def create_bilingual_log_entry(
    log_entry: Dict[str, Any], target_language: str = "en"
) -> Dict[str, Any]:
    """Create a log entry with both original and translated text."""

    # Translate the message field
    if "message" in log_entry and log_entry["message"]:
        translation_result = translate_log_message(
            log_entry["message"], target_language_code=target_language
        )

        if translation_result["translation"].get("translated_text"):
            # Create bilingual entry
            bilingual_entry = log_entry.copy()
            bilingual_entry["message_original"] = log_entry["message"]
            bilingual_entry["message_translated"] = translation_result["translation"][
                "translated_text"
            ]
            bilingual_entry["translation_language"] = target_language
            bilingual_entry["translation_source_language"] = translation_result[
                "translation"
            ].get("source_language", "auto")
            bilingual_entry["translation_provider"] = "Amazon Translate"

            return bilingual_entry

    # Return original if translation fails
    return log_entry


if __name__ == "__main__":
    # Example usage
    test_log_message = (
        "Error: La conexión a la base de datos ha fallado debido a un timeout."
    )

    result = translate_log_message(
        text=test_log_message, source_language_code="auto", target_language_code="en"
    )

    print("Translation Result:")
    print(json.dumps(result, indent=2))

    # Batch example
    test_logs = [
        {
            "id": "log1",
            "message": "Erreur: Échec de l'authentification",
            "severity": "ERROR",
        },
        {
            "id": "log2",
            "message": "Avis: Utilisateur connecté avec succès",
            "severity": "INFO",
        },
        {
            "id": "log3",
            "message": "Error: Database connection timeout",
            "severity": "ERROR",
        },
    ]

    batch_result = translate_logs_batch(
        log_entries=test_logs,
        target_language_code="en",
        fields_to_translate=["message"],
    )

    print("\nBatch Translation Summary:")
    print(json.dumps(batch_result["summary"], indent=2))
