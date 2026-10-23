import os
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError


def translate_consent_text_with_amazon(
    text: str, source_language: str, target_language: str, context: str = None
) -> Dict[str, Any]:
    """
    Translate identity-provider consent copy using Amazon Translate.
    """
    # Check for AWS credentials
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    # Create Translate client
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    try:
        # Prepare translation parameters
        translation_params = {
            "Text": text,
            "SourceLanguageCode": source_language,
            "TargetLanguageCode": target_language,
        }

        # Add terminology if context is provided
        if context == "consent" or context == "legal":
            # For consent/legal text, we might want to use specific terminology
            # In production, you would configure a custom terminology in AWS Translate
            pass

        # Call Amazon Translate
        response = translate_client.translate_text(**translation_params)

        result = {
            "original_text": text,
            "translated_text": response["TranslatedText"],
            "source_language": response["SourceLanguageCode"],
            "target_language": response["TargetLanguageCode"],
            "provider": "amazon_translate",
            "context": context,
            "applied_terminology": response.get("AppliedTerminologies", []),
            "confidence": 0.95,  # Amazon Translate doesn't provide confidence score in response
        }

        return result

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        # Fallback to basic translation or return error
        return {
            "original_text": text,
            "translated_text": f"[Translation Error: {error_code}] {text}",
            "source_language": source_language,
            "target_language": target_language,
            "provider": "amazon_translate_error",
            "context": context,
            "error": error_message,
            "error_code": error_code,
            "confidence": 0.0,
        }


def translate_multiple_consent_texts(
    translations: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Translate multiple consent texts in batch.
    Each item should have 'text', 'source_language', 'target_language', and optional 'context'.
    """
    results = []

    for translation_request in translations:
        text = translation_request.get("text", "")
        source_lang = translation_request.get("source_language", "en")
        target_lang = translation_request.get("target_language", "es")
        context = translation_request.get("context")

        result = translate_consent_text_with_amazon(
            text, source_lang, target_lang, context
        )
        results.append(result)

    return results


def get_supported_languages() -> Dict[str, Any]:
    """
    Get list of languages supported by Amazon Translate.
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

    try:
        # Get list of supported languages
        response = translate_client.list_languages()

        languages = []
        for lang in response["Languages"]:
            languages.append(
                {
                    "language_code": lang["LanguageCode"],
                    "language_name": lang["LanguageName"],
                }
            )

        return {
            "provider": "amazon_translate",
            "supported_languages": languages,
            "count": len(languages),
        }

    except ClientError as e:
        # Return a subset of commonly supported languages as fallback
        common_languages = [
            {"language_code": "en", "language_name": "English"},
            {"language_code": "es", "language_name": "Spanish"},
            {"language_code": "fr", "language_name": "French"},
            {"language_code": "de", "language_name": "German"},
            {"language_code": "it", "language_name": "Italian"},
            {"language_code": "pt", "language_name": "Portuguese"},
            {"language_code": "ja", "language_name": "Japanese"},
            {"language_code": "ko", "language_name": "Korean"},
            {"language_code": "zh", "language_name": "Chinese (Simplified)"},
            {"language_code": "ar", "language_name": "Arabic"},
        ]

        return {
            "provider": "amazon_translate_fallback",
            "supported_languages": common_languages,
            "count": len(common_languages),
            "note": "Using fallback language list due to API error",
        }


def validate_translation_quality(
    original: str, translated: str, source_lang: str, target_lang: str
) -> Dict[str, Any]:
    """
    Basic validation of translation quality.
    In production, you might use additional services or human review.
    """
    # Basic checks
    issues = []

    # Check if translation is empty
    if not translated or translated.strip() == "":
        issues.append("Empty translation")

    # Check if translation is same as original (might indicate failure)
    if translated == original and source_lang != target_lang:
        issues.append("Translation identical to original")

    # Check for placeholder text
    if "[Translation Error" in translated or "ERROR" in translated.upper():
        issues.append("Contains error placeholder")

    # Check length ratio (very rough quality indicator)
    orig_len = len(original)
    trans_len = len(translated)

    if orig_len > 0:
        ratio = trans_len / orig_len
        if ratio < 0.1 or ratio > 10:  # Extreme ratios might indicate issues
            issues.append(f"Extreme length ratio: {ratio:.2f}")

    quality_score = 1.0 - (len(issues) * 0.2)  # Simple scoring
    quality_score = max(0.0, min(1.0, quality_score))

    return {
        "quality_score": quality_score,
        "issues": issues,
        "original_length": orig_len,
        "translated_length": trans_len,
        "length_ratio": trans_len / orig_len if orig_len > 0 else 0,
    }
