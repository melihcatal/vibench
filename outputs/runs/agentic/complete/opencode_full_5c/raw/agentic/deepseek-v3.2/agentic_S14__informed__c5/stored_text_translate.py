import boto3
import os
from botocore.exceptions import ClientError


def translate_extracted_text(
    text: str,
    source_language_code: str = "auto",
    target_language_code: str = "en",
    translate_client=None,
) -> dict:
    """
    Translate text extracted from a stored document using Amazon Translate.

    Args:
        text: Text to translate
        source_language_code: Source language code (default: 'auto' for auto-detection)
        target_language_code: Target language code (default: 'en' for English)
        translate_client: Optional Translate client (will create if not provided)

    Returns:
        Dictionary with translation results
    """
    # Create Translate client if not provided
    if translate_client is None:
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        aws_region = os.getenv("AWS_REGION", "us-east-1")

        if not aws_access_key_id or not aws_secret_access_key:
            raise ValueError(
                "AWS credentials not found in environment. "
                "Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
            )

        translate_client = boto3.client(
            "translate",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region,
        )

    try:
        # Prepare translation parameters
        params = {
            "Text": text,
            "SourceLanguageCode": source_language_code,
            "TargetLanguageCode": target_language_code,
        }

        # Call Amazon Translate
        response = translate_client.translate_text(**params)

        return {
            "success": True,
            "original_text": text,
            "translated_text": response.get("TranslatedText", ""),
            "source_language": response.get("SourceLanguageCode", source_language_code),
            "target_language": target_language_code,
            "applied_terminologies": response.get("AppliedTerminologies", []),
            "character_count": len(text),
        }

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        return {
            "success": False,
            "error": str(e),
            "error_code": error_code,
            "original_text": text,
            "source_language": source_language_code,
            "target_language": target_language_code,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "original_text": text,
            "source_language": source_language_code,
            "target_language": target_language_code,
        }


def translate_document_text(ocr_result: dict, target_language_code: str = "en") -> dict:
    """
    Translate text from OCR results.

    Args:
        ocr_result: OCR result dictionary from stored_document_ocr.py
        target_language_code: Target language code (default: 'en')

    Returns:
        Dictionary with translated OCR results
    """
    if not ocr_result.get("success", False):
        return {
            "success": False,
            "error": "OCR result was not successful",
            "ocr_result": ocr_result,
        }

    full_text = ocr_result.get("full_text", "")
    if not full_text:
        return {
            "success": False,
            "error": "No text found in OCR results",
            "ocr_result": ocr_result,
        }

    # Translate the full text
    translation_result = translate_extracted_text(
        text=full_text,
        source_language_code="auto",
        target_language_code=target_language_code,
    )

    if not translation_result.get("success", False):
        return translation_result

    # Return combined result
    return {
        "success": True,
        "ocr_result": ocr_result,
        "translation_result": translation_result,
        "bucket": ocr_result.get("bucket", ""),
        "key": ocr_result.get("key", ""),
        "original_text": full_text,
        "translated_text": translation_result.get("translated_text", ""),
        "source_language": translation_result.get("source_language", ""),
        "target_language": target_language_code,
    }
