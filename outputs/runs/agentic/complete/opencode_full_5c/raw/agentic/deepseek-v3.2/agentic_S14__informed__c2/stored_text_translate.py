import boto3
import os
from botocore.exceptions import ClientError
from storage_models import TranslationResult


def translate_extracted_text(text, target_language_code, source_language_code="auto"):
    """
    Translate text extracted from a stored document using Amazon Translate.

    Args:
        text: Text to translate
        target_language_code: Target language code (e.g., 'es', 'fr', 'de')
        source_language_code: Source language code or 'auto' for auto-detection

    Returns:
        dict: Translation results or error
    """
    translate_client = boto3.client("translate")

    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code,
        )

        return {
            "success": True,
            "source_text": text,
            "translated_text": response["TranslatedText"],
            "source_language": response.get("SourceLanguageCode", source_language_code),
            "target_language": target_language_code,
            "provider": "Amazon Translate",
            "model": "amazon-translate-standard",
        }

    except ClientError as e:
        return {"success": False, "error": str(e), "provider": "Amazon Translate"}
    except Exception as e:
        return {"success": False, "error": str(e), "provider": "Amazon Translate"}


def translate_document_from_storage(
    bucket_name, object_key, target_language_code, source_language_code="auto"
):
    """
    Extract text from stored document and translate it.

    Args:
        bucket_name: S3 bucket name
        object_key: S3 object key
        target_language_code: Target language code
        source_language_code: Source language code

    Returns:
        dict: Combined OCR and translation results
    """
    # First run OCR to extract text
    from stored_document_ocr import run_ocr_on_stored_document

    ocr_result = run_ocr_on_stored_document(bucket_name, object_key)

    if not ocr_result.get("success"):
        return {
            "success": False,
            "error": f"OCR failed: {ocr_result.get('error')}",
            "provider": "Amazon Translate + Textract",
        }

    # Translate the extracted text
    text_to_translate = ocr_result.get("text", "")
    if not text_to_translate:
        return {
            "success": False,
            "error": "No text extracted from document",
            "provider": "Amazon Translate + Textract",
        }

    translation_result = translate_extracted_text(
        text_to_translate, target_language_code, source_language_code
    )

    if translation_result.get("success"):
        return {
            "success": True,
            "ocr_result": {
                "text": text_to_translate,
                "confidence": ocr_result.get("confidence"),
                "pages": ocr_result.get("pages", []),
            },
            "translation_result": {
                "translated_text": translation_result.get("translated_text"),
                "source_language": translation_result.get("source_language"),
                "target_language": translation_result.get("target_language"),
            },
            "provider": "Amazon Translate + Textract",
        }
    else:
        return {
            "success": False,
            "error": f"Translation failed: {translation_result.get('error')}",
            "ocr_success": True,
            "extracted_text": text_to_translate,
            "provider": "Amazon Translate + Textract",
        }
