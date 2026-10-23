import os
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError


def translate_invoice_notes(
    notes_text: str, target_language: str = "en", source_language: str = "auto"
) -> Dict[str, Any]:
    """
    Translate extracted invoice notes or descriptions using Amazon Translate.

    Args:
        notes_text: Text to translate
        target_language: Target language code (default: 'en' for English)
        source_language: Source language code or 'auto' for auto-detection

    Returns:
        Translation results
    """
    # Create Amazon Translate client
    translate_client = boto3.client(
        "translate",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        # Call Amazon Translate
        response = translate_client.translate_text(
            Text=notes_text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )

        # Parse response
        translation_result = {
            "original_text": notes_text,
            "translated_text": response["TranslatedText"],
            "source_language": response.get("SourceLanguageCode", source_language),
            "target_language": target_language,
            "provider": "Amazon Translate",
            "aws_service": "translate.translate_text",
            "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        }

        # Add language confidence if available
        if "AppliedTerminologies" in response:
            translation_result["terminologies_applied"] = response[
                "AppliedTerminologies"
            ]

        return translation_result

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        raise Exception(f"Amazon Translate error ({error_code}): {error_message}")
    except Exception as e:
        raise Exception(f"Translation error: {e}")


def translate_multiple_descriptions(
    descriptions: List[str], target_language: str = "en"
) -> List[Dict[str, Any]]:
    """
    Translate multiple invoice descriptions.

    Args:
        descriptions: List of description texts to translate
        target_language: Target language code

    Returns:
        List of translation results
    """
    results = []

    for desc in descriptions:
        if desc and desc.strip():
            try:
                translation = translate_invoice_notes(desc, target_language)
                results.append(translation)
            except Exception as e:
                results.append(
                    {
                        "original_text": desc,
                        "error": str(e),
                        "translated_text": None,
                        "provider": "Amazon Translate",
                    }
                )

    return results
