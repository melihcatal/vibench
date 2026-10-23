import os
import json
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError


def translate_dashboard_note(
    text: str, source_language_code: str, target_language_code: str
) -> Dict[str, Any]:
    """
    Translate metric or dashboard notes using Amazon Translate.

    Args:
        text: Text to translate
        source_language_code: Source language code (e.g., "en", "es", "fr")
        target_language_code: Target language code (e.g., "en", "es", "fr")

    Returns:
        Translation results
    """
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    translate_client = session.client("translate")

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )

        return {
            "original_text": text,
            "translated_text": response["TranslatedText"],
            "source_language": response.get("SourceLanguageCode", source_language_code),
            "target_language": target_language_code,
            "service_used": "Amazon Translate",
            "character_count": len(text),
            "translation_metadata": {
                "applied_terminologies": response.get("AppliedTerminologies", []),
                "applied_settings": response.get("AppliedSettings", {}),
            },
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        if error_code == "UnsupportedLanguagePairException":
            return {
                "original_text": text,
                "error": f"Translation from {source_language_code} to {target_language_code} not supported",
                "source_language": source_language_code,
                "target_language": target_language_code,
                "service_used": "Amazon Translate",
            }
        else:
            raise


def translate_metric_annotations(
    annotations: Dict[str, str],
    target_language_code: str,
    source_language_code: str = "auto",
) -> Dict[str, Any]:
    """
    Translate multiple metric annotations.

    Args:
        annotations: Dictionary of annotation keys and values
        target_language_code: Target language code
        source_language_code: Source language code or "auto" for automatic detection

    Returns:
        Translation results for all annotations
    """
    results = {}
    translation_stats = {
        "total_annotations": len(annotations),
        "successful_translations": 0,
        "failed_translations": 0,
        "total_characters": 0,
    }

    for key, text in annotations.items():
        if not text or not isinstance(text, str):
            results[key] = {
                "original_text": text,
                "error": "Empty or non-string text",
                "skipped": True,
            }
            continue

        try:
            result = translate_dashboard_note(
                text=text,
                source_language_code=source_language_code,
                target_language_code=target_language_code,
            )

            results[key] = result

            if "error" not in result:
                translation_stats["successful_translations"] += 1
                translation_stats["total_characters"] += len(text)
            else:
                translation_stats["failed_translations"] += 1

        except Exception as e:
            results[key] = {"original_text": text, "error": str(e), "skipped": True}
            translation_stats["failed_translations"] += 1

    return {
        "translation_summary": translation_stats,
        "target_language": target_language_code,
        "source_language": source_language_code,
        "detailed_results": results,
        "all_successful": translation_stats["failed_translations"] == 0,
    }


def detect_language(text: str) -> Dict[str, Any]:
    """
    Detect the language of text using Amazon Translate.

    Args:
        text: Text to analyze

    Returns:
        Language detection results
    """
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    translate_client = session.client("translate")

    try:
        response = translate_client.translate_text(
            Text=text, SourceLanguageCode="auto", TargetLanguageCode="en"
        )

        return {
            "text": text,
            "detected_language": response.get("SourceLanguageCode", "unknown"),
            "confidence": "high",
            "service_used": "Amazon Translate Language Detection",
        }

    except ClientError as e:
        return {
            "text": text,
            "error": str(e),
            "service_used": "Amazon Translate Language Detection",
        }


def translate_with_fallback(
    text: str, target_language_code: str, fallback_languages: List[str] = None
) -> Dict[str, Any]:
    """
    Translate text with fallback language support.

    Args:
        text: Text to translate
        target_language_code: Primary target language
        fallback_languages: List of fallback languages if primary fails

    Returns:
        Translation results with fallback information
    """
    if fallback_languages is None:
        fallback_languages = ["en", "es", "fr"]

    language_detection = detect_language(text)
    source_language = language_detection.get("detected_language", "auto")

    if source_language == target_language_code:
        return {
            "original_text": text,
            "translated_text": text,
            "source_language": source_language,
            "target_language": target_language_code,
            "note": "Source and target languages are the same",
            "service_used": "Amazon Translate",
        }

    try:
        return translate_dashboard_note(text, source_language, target_language_code)
    except ClientError as e:
        if e.response["Error"]["Code"] == "UnsupportedLanguagePairException":
            for fallback_lang in fallback_languages:
                if fallback_lang != target_language_code:
                    try:
                        result = translate_dashboard_note(
                            text, source_language, fallback_lang
                        )
                        result["fallback_used"] = True
                        result["original_target"] = target_language_code
                        result["actual_target"] = fallback_lang
                        return result
                    except:
                        continue

            return {
                "original_text": text,
                "error": f"Could not translate from {source_language} to {target_language_code} or any fallback language",
                "source_language": source_language,
                "target_language": target_language_code,
                "fallback_languages_tried": fallback_languages,
                "service_used": "Amazon Translate",
            }
        else:
            raise


if __name__ == "__main__":
    test_note = "CPU utilization is above threshold. Consider scaling up the instance."

    translation = translate_dashboard_note(
        text=test_note, source_language_code="en", target_language_code="es"
    )

    print(f"Translation result: {json.dumps(translation, indent=2, default=str)}")

    test_annotations = {
        "title": "Production Dashboard",
        "description": "Monitor production server metrics",
        "warning": "High CPU usage detected",
    }

    batch_result = translate_metric_annotations(
        annotations=test_annotations, target_language_code="fr"
    )

    print(f"\nBatch translation successful: {batch_result['all_successful']}")
