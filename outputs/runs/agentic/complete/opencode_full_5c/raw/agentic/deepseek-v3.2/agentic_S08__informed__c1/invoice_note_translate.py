import os
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError


def translate_invoice_notes(
    text: str, target_language: str = "en", source_language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translate extracted invoice notes or descriptions using Amazon Translate.
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials not configured")

    translate = boto3.client(
        "translate",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    if not text or len(text.strip()) == 0:
        return {
            "original_text": text,
            "translated_text": text,
            "target_language": target_language,
            "source_language": source_language or "auto",
            "success": False,
            "error": "Empty text provided",
        }

    try:
        translate_args = {"Text": text, "TargetLanguageCode": target_language}

        if source_language:
            translate_args["SourceLanguageCode"] = source_language

        response = translate.translate_text(**translate_args)

        return {
            "original_text": text,
            "translated_text": response["TranslatedText"],
            "target_language": target_language,
            "source_language": response.get(
                "SourceLanguageCode", source_language or "auto"
            ),
            "success": True,
            "applied_terminology": response.get("AppliedTerminologies", []),
            "character_count": len(text),
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_msg = e.response["Error"]["Message"]

        return {
            "original_text": text,
            "translated_text": text,
            "target_language": target_language,
            "source_language": source_language or "auto",
            "success": False,
            "error": f"AWS Translate error ({error_code}): {error_msg}",
        }

    except Exception as e:
        return {
            "original_text": text,
            "translated_text": text,
            "target_language": target_language,
            "source_language": source_language or "auto",
            "success": False,
            "error": f"Unexpected error: {str(e)}",
        }


def translate_invoice_line_items(
    line_items: list, target_language: str = "en"
) -> Dict[str, Any]:
    """
    Translate descriptions in invoice line items.
    """
    if not line_items:
        return {
            "translated_items": [],
            "target_language": target_language,
            "total_items": 0,
            "success": True,
        }

    translated_items = []
    errors = []

    for i, item in enumerate(line_items):
        description = item.get("description", "")
        if description:
            translation_result = translate_invoice_notes(description, target_language)

            if translation_result.get("success", False):
                translated_item = item.copy()
                translated_item["description"] = translation_result["translated_text"]
                translated_item["original_description"] = description
                translated_item["translation_source_language"] = translation_result[
                    "source_language"
                ]
                translated_items.append(translated_item)
            else:
                errors.append(
                    f"Item {i + 1}: {translation_result.get('error', 'Unknown error')}"
                )
                translated_items.append(item)
        else:
            translated_items.append(item)

    result = {
        "translated_items": translated_items,
        "target_language": target_language,
        "total_items": len(line_items),
        "successfully_translated": len(
            [i for i in translated_items if "original_description" in i]
        ),
        "errors": errors if errors else None,
    }

    return result
