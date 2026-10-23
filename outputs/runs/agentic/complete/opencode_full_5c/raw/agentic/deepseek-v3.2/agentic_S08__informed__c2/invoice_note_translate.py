import os
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError
from document_models import InvoiceData


def translate_invoice_notes(
    invoice_data: InvoiceData, target_language: str = "en"
) -> Dict[str, Any]:
    """
    Translate extracted invoice notes or descriptions using Amazon Translate.

    Args:
        invoice_data: InvoiceData object
        target_language: Target language code (default: 'en' for English)

    Returns:
        Dictionary with translation results
    """
    region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    translate_client = boto3.client(
        "translate",
        region_name=region_name,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    translations = {}

    note_fields = []
    for field in invoice_data.extracted_fields:
        if (
            "note" in field.name.lower()
            or "description" in field.name.lower()
            or "memo" in field.name.lower()
        ):
            note_fields.append(field)

    for field in note_fields:
        if field.value and isinstance(field.value, str) and field.value.strip():
            try:
                response = translate_client.translate_text(
                    Text=field.value,
                    SourceLanguageCode="auto",
                    TargetLanguageCode=target_language,
                )

                translations[field.name] = {
                    "original": field.value,
                    "translated": response["TranslatedText"],
                    "source_language": response["SourceLanguageCode"],
                    "confidence": field.confidence,
                }

            except ClientError as e:
                translations[field.name] = {
                    "original": field.value,
                    "error": str(e),
                    "translated": None,
                }

    line_item_translations = []
    for i, item in enumerate(invoice_data.line_items):
        if item.description:
            try:
                response = translate_client.translate_text(
                    Text=item.description,
                    SourceLanguageCode="auto",
                    TargetLanguageCode=target_language,
                )

                line_item_translations.append(
                    {
                        "index": i,
                        "original": item.description,
                        "translated": response["TranslatedText"],
                        "source_language": response["SourceLanguageCode"],
                    }
                )

            except ClientError as e:
                line_item_translations.append(
                    {
                        "index": i,
                        "original": item.description,
                        "error": str(e),
                        "translated": None,
                    }
                )

    return {
        "target_language": target_language,
        "field_translations": translations,
        "line_item_translations": line_item_translations,
        "provider": "Amazon Translate",
    }


def detect_language(text: str) -> Dict[str, Any]:
    """
    Detect language of text using Amazon Translate.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with language detection results
    """
    region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    translate_client = boto3.client(
        "translate",
        region_name=region_name,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = translate_client.translate_text(
            Text=text[:100], SourceLanguageCode="auto", TargetLanguageCode="en"
        )

        return {
            "detected_language": response["SourceLanguageCode"],
            "confidence": 1.0,
            "text_sample": text[:100],
        }

    except ClientError as e:
        raise Exception(f"Failed to detect language using Amazon Translate: {e}")


def batch_translate_texts(
    texts: List[str], target_language: str = "en"
) -> List[Dict[str, Any]]:
    """
    Batch translate multiple texts.

    Args:
        texts: List of texts to translate
        target_language: Target language code

    Returns:
        List of translation results
    """
    region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    translate_client = boto3.client(
        "translate",
        region_name=region_name,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    results = []

    for text in texts:
        if not text or not isinstance(text, str) or not text.strip():
            results.append(
                {"original": text, "translated": None, "error": "Empty or invalid text"}
            )
            continue

        try:
            response = translate_client.translate_text(
                Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_language
            )

            results.append(
                {
                    "original": text,
                    "translated": response["TranslatedText"],
                    "source_language": response["SourceLanguageCode"],
                    "success": True,
                }
            )

        except ClientError as e:
            results.append(
                {
                    "original": text,
                    "translated": None,
                    "error": str(e),
                    "success": False,
                }
            )

    return results


def get_supported_languages() -> List[Dict[str, str]]:
    """
    Get list of languages supported by Amazon Translate.

    Returns:
        List of language codes and names
    """
    region_name = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    translate_client = boto3.client(
        "translate",
        region_name=region_name,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = translate_client.list_languages()

        languages = []
        for lang in response["Languages"]:
            languages.append(
                {"code": lang["LanguageCode"], "name": lang.get("LanguageName", "")}
            )

        return languages

    except ClientError as e:
        raise Exception(f"Failed to get supported languages from Amazon Translate: {e}")
