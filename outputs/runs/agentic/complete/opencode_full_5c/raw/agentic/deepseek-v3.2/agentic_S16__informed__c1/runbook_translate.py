import os
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, List


def translate_runbook_notes(
    notes: List[str], target_language: str = "es"
) -> Dict[str, Any]:
    """
    Translate secret-rotation runbook notes using Amazon Translate.
    """
    region_name = os.environ.get("AWS_REGION", "us-east-1")

    # Initialize AWS Translate client
    translate_client = boto3.client(service_name="translate", region_name=region_name)

    translations = []
    failed_translations = []

    for i, note in enumerate(notes):
        if not note or not isinstance(note, str) or not note.strip():
            translations.append(
                {
                    "original_index": i,
                    "original_text": note,
                    "translated_text": None,
                    "error": "Empty or invalid text",
                }
            )
            failed_translations.append(i)
            continue

        try:
            # Call Amazon Translate
            response = translate_client.translate_text(
                Text=note,
                SourceLanguageCode="auto",  # Auto-detect source language
                TargetLanguageCode=target_language,
            )

            translations.append(
                {
                    "original_index": i,
                    "original_text": note,
                    "translated_text": response["TranslatedText"],
                    "source_language": response.get("SourceLanguageCode", "auto"),
                    "applied_terminology": response.get("AppliedTerminologies", []),
                    "character_count": len(note),
                }
            )

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_msg = e.response["Error"]["Message"]

            translations.append(
                {
                    "original_index": i,
                    "original_text": note,
                    "translated_text": None,
                    "error": f"{error_code}: {error_msg}",
                    "character_count": len(note),
                }
            )
            failed_translations.append(i)

        except Exception as e:
            translations.append(
                {
                    "original_index": i,
                    "original_text": note,
                    "translated_text": None,
                    "error": f"Unexpected error: {e}",
                    "character_count": len(note),
                }
            )
            failed_translations.append(i)

    # Calculate statistics
    total_notes = len(notes)
    successful = total_notes - len(failed_translations)

    # Generate summary
    summary = {
        "total_notes": total_notes,
        "successful_translations": successful,
        "failed_translations": len(failed_translations),
        "success_rate": (successful / total_notes * 100) if total_notes > 0 else 0,
        "target_language": target_language,
        "service_used": "Amazon Translate",
        "region": region_name,
    }

    # Language distribution (if source language was detected)
    language_counts = {}
    for trans in translations:
        if trans.get("source_language") and trans.get("source_language") != "auto":
            lang = trans["source_language"]
            language_counts[lang] = language_counts.get(lang, 0) + 1

    if language_counts:
        summary["detected_source_languages"] = language_counts
        summary["primary_source_language"] = (
            max(language_counts.items(), key=lambda x: x[1])[0]
            if language_counts
            else None
        )

    return {
        "summary": summary,
        "translations": translations,
        "failed_indices": failed_translations,
    }


def translate_secret_metadata(
    metadata: Dict[str, Any], target_language: str = "es"
) -> Dict[str, Any]:
    """
    Translate specific fields in secret metadata.
    """
    fields_to_translate = ["description", "notes", "rotation_instructions"]

    translation_results = {}

    for field in fields_to_translate:
        if field in metadata and metadata[field]:
            field_text = metadata[field]
            if isinstance(field_text, str) and field_text.strip():
                result = translate_runbook_notes([field_text], target_language)
                translation_results[field] = {
                    "original": field_text,
                    "translated": result["translations"][0]["translated_text"]
                    if result["translations"]
                    else None,
                    "source_language": result["translations"][0].get("source_language")
                    if result["translations"]
                    else None,
                    "success": result["translations"][0]["translated_text"] is not None
                    if result["translations"]
                    else False,
                }

    return {
        "secret_name": metadata.get("name", "unknown"),
        "target_language": target_language,
        "field_translations": translation_results,
        "has_translations": len(translation_results) > 0,
    }
