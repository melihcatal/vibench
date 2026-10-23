import os
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError


def translate_platform_output(
    text: str, source_language: str = "auto", target_language: str = "es"
) -> Dict[str, Any]:
    """Translate platform model output for another locale using Amazon Translate."""

    # Initialize AWS Translate client
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        # Use Amazon Translate API
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )

        # Extract translation results
        translated_text = response["TranslatedText"]
        detected_source_language = response["SourceLanguageCode"]

        # Get additional metadata if available
        applied_terminologies = response.get("AppliedTerminologies", [])

        return {
            "provider": "amazon-translate",
            "service": "TranslateText",
            "original_text": text,
            "translated_text": translated_text,
            "source_language": detected_source_language,
            "target_language": target_language,
            "character_count": len(text),
            "applied_terminologies": applied_terminologies,
            "request_id": response.get("ResponseMetadata", {}).get("RequestId", ""),
        }

    except ClientError as e:
        print(f"Amazon Translate error: {e}")

        # Fallback to basic translation placeholder
        return {
            "provider": "fallback-basic",
            "service": "placeholder-translation",
            "original_text": text,
            "translated_text": f"[Translation to {target_language} placeholder: {text[:50]}...]",
            "source_language": source_language,
            "target_language": target_language,
            "error": str(e),
            "warning": "Amazon Translate service unavailable, using placeholder",
        }


def batch_translate_platform_outputs(
    texts: List[str], source_language: str = "auto", target_language: str = "es"
) -> List[Dict[str, Any]]:
    """Translate multiple platform outputs using Amazon Translate batch processing."""

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    results = []

    for i, text in enumerate(texts):
        try:
            # Process each text individually (batch API would be better for large volumes)
            result = translate_platform_output(text, source_language, target_language)
            result["item_index"] = i
            results.append(result)
        except Exception as e:
            # Add error result for failed translations
            results.append(
                {
                    "provider": "amazon-translate",
                    "service": "TranslateText",
                    "original_text": text,
                    "error": str(e),
                    "item_index": i,
                    "success": False,
                }
            )

    return results


def get_supported_languages() -> List[Dict[str, str]]:
    """Get list of languages supported by Amazon Translate."""

    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        response = translate_client.list_languages()
        languages = response["Languages"]

        # Format languages for display
        formatted_languages = []
        for lang in languages:
            formatted_languages.append(
                {
                    "language_code": lang["LanguageCode"],
                    "language_name": lang.get("LanguageName", "Unknown"),
                }
            )

        return formatted_languages

    except ClientError as e:
        print(f"Error getting supported languages: {e}")

        # Return common languages as fallback
        return [
            {"language_code": "en", "language_name": "English"},
            {"language_code": "es", "language_name": "Spanish"},
            {"language_code": "fr", "language_name": "French"},
            {"language_code": "de", "language_name": "German"},
            {"language_code": "ja", "language_name": "Japanese"},
            {"language_code": "zh", "language_name": "Chinese"},
            {"language_code": "ar", "language_name": "Arabic"},
        ]
