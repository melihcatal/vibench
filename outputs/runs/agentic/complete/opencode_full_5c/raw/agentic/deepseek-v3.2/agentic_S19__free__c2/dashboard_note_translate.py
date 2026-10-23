import os
from typing import Dict, List, Optional
import boto3
from botocore.exceptions import ClientError


def translate_dashboard_notes(
    text: str, target_language_code: str, source_language_code: Optional[str] = None
) -> Dict[str, any]:
    """
    Translate metric or dashboard notes for another locale using Amazon Translate.

    Args:
        text: The text to translate
        target_language_code: Target language code (e.g., 'es', 'fr', 'de')
        source_language_code: Source language code (optional, auto-detected if None)

    Returns:
        Dictionary with translation results
    """
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    supported_languages = [
        "af",
        "sq",
        "am",
        "ar",
        "hy",
        "az",
        "bn",
        "bs",
        "bg",
        "ca",
        "zh",
        "zh-TW",
        "hr",
        "cs",
        "da",
        "fa-AF",
        "nl",
        "en",
        "et",
        "fa",
        "tl",
        "fi",
        "fr",
        "fr-CA",
        "ka",
        "de",
        "el",
        "gu",
        "ht",
        "ha",
        "he",
        "hi",
        "hu",
        "is",
        "id",
        "ga",
        "it",
        "ja",
        "kn",
        "kk",
        "ko",
        "lv",
        "lt",
        "mk",
        "ms",
        "ml",
        "mt",
        "mr",
        "mn",
        "no",
        "ps",
        "pl",
        "pt",
        "pt-PT",
        "pa",
        "ro",
        "ru",
        "sr",
        "si",
        "sk",
        "sl",
        "so",
        "es",
        "es-MX",
        "sw",
        "sv",
        "ta",
        "te",
        "th",
        "tr",
        "uk",
        "ur",
        "uz",
        "vi",
        "cy",
    ]

    if target_language_code not in supported_languages:
        raise ValueError(
            f"Unsupported target language code: {target_language_code}. Supported: {supported_languages[:10]}..."
        )

    try:
        translate_params = {
            "Text": text,
            "SourceLanguageCode": source_language_code or "auto",
            "TargetLanguageCode": target_language_code,
        }

        response = translate_client.translate_text(**translate_params)

        result = {
            "original_text": text,
            "translated_text": response["TranslatedText"],
            "source_language": response["SourceLanguageCode"],
            "target_language": target_language_code,
            "success": True,
            "character_count": len(text),
            "service": "Amazon Translate",
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        result = {
            "original_text": text,
            "translated_text": None,
            "source_language": source_language_code or "auto",
            "target_language": target_language_code,
            "success": False,
            "error": {"code": error_code, "message": error_message},
            "service": "Amazon Translate",
        }

    return result


def translate_metric_labels(
    metric_data: List[Dict[str, any]], target_language_code: str
) -> List[Dict[str, any]]:
    """
    Translate metric labels and annotations in metric data.

    Args:
        metric_data: List of metric datapoints with labels/annotations
        target_language_code: Target language code

    Returns:
        List of metric datapoints with translated labels
    """
    translated_data = []

    for item in metric_data:
        translated_item = item.copy()

        if "metric_labels" in item and item["metric_labels"]:
            translated_labels = {}
            for key, value in item["metric_labels"].items():
                if isinstance(value, str) and value.strip():
                    translation = translate_dashboard_notes(value, target_language_code)
                    if translation["success"]:
                        translated_labels[key] = translation["translated_text"]
                    else:
                        translated_labels[key] = value
                else:
                    translated_labels[key] = value
            translated_item["metric_labels"] = translated_labels

        if "resource_labels" in item and item["resource_labels"]:
            translated_resource_labels = {}
            for key, value in item["resource_labels"].items():
                if (
                    isinstance(value, str)
                    and value.strip()
                    and not value.replace(".", "").isdigit()
                ):
                    translation = translate_dashboard_notes(value, target_language_code)
                    if translation["success"]:
                        translated_resource_labels[key] = translation["translated_text"]
                    else:
                        translated_resource_labels[key] = value
                else:
                    translated_resource_labels[key] = value
            translated_item["resource_labels"] = translated_resource_labels

        translated_data.append(translated_item)

    return translated_data


def batch_translate_notes(
    notes: List[str], target_language_code: str
) -> Dict[str, any]:
    """
    Translate multiple notes in a batch.

    Args:
        notes: List of notes to translate
        target_language_code: Target language code

    Returns:
        Dictionary with batch translation results
    """
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    results = {
        "total_notes": len(notes),
        "successful_translations": 0,
        "failed_translations": 0,
        "translations": [],
        "target_language": target_language_code,
    }

    for note in notes:
        try:
            translation = translate_dashboard_notes(note, target_language_code)
            results["translations"].append(translation)

            if translation["success"]:
                results["successful_translations"] += 1
            else:
                results["failed_translations"] += 1

        except Exception as e:
            results["translations"].append(
                {"original_text": note, "success": False, "error": str(e)}
            )
            results["failed_translations"] += 1

    return results


if __name__ == "__main__":
    sample_notes = [
        "CPU utilization is above threshold",
        "Memory usage normal",
        "Network latency increased",
        "Disk I/O operations per second",
    ]

    try:
        for note in sample_notes:
            translation = translate_dashboard_notes(note, "es")
            print(f"Original: {note}")
            print(f"Translated: {translation['translated_text']}")
            print(f"Source language: {translation['source_language']}")
            print()

        batch_result = batch_translate_notes(sample_notes[:2], "fr")
        print(
            f"Batch translation: {batch_result['successful_translations']}/{batch_result['total_notes']} successful"
        )

    except Exception as e:
        print(f"Error translating dashboard notes: {e}")
