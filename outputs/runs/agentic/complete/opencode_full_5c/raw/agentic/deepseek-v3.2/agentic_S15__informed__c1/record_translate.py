import os
import boto3
from typing import Dict, List, Any
from botocore.exceptions import ClientError
from database_models import TranslationRequest, TranslationResponse, TranslationResult

# AWS Translate configuration
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Translate client cache
_translate_client = None


def get_translate_client():
    """
    Get or create an AWS Translate client.
    """
    global _translate_client

    if _translate_client is None:
        client_kwargs = {"region_name": AWS_REGION}

        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            client_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
            client_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY

        _translate_client = boto3.client("translate", **client_kwargs)

    return _translate_client


def translate_record_fields(request: TranslationRequest) -> TranslationResponse:
    """
    Translate user-facing document fields using AWS Translate.
    """
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        return TranslationResponse(
            success=False,
            document_id=request.document_id,
            results=[],
            error="AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required",
            timestamp=request.timestamp,
        )

    try:
        translate = get_translate_client()
        results = []

        for field_name, target_language in request.translations.items():
            original_text = request.document_data.get(field_name, "")

            if not original_text or not isinstance(original_text, str):
                # Skip non-string or empty fields
                results.append(
                    TranslationResult(
                        field_name=field_name,
                        original_text=str(original_text)[:100] + "..."
                        if original_text
                        else "",
                        translated_text=str(original_text)[:100] + "..."
                        if original_text
                        else "",
                        target_language=target_language,
                        detected_language=None,
                    )
                )
                continue

            # Truncate text if too long (Translate has limits)
            if len(original_text) > 5000:
                original_text = original_text[:5000]

            # Determine source language
            source_language_code = request.source_language or "auto"

            # Call AWS Translate
            response = translate.translate_text(
                Text=original_text,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language,
            )

            # Extract results
            translated_text = response["TranslatedText"]
            detected_language = response.get("SourceLanguageCode")

            # If auto-detection was used and we got a result, update source language
            if source_language_code == "auto" and detected_language:
                source_language_code = detected_language

            results.append(
                TranslationResult(
                    field_name=field_name,
                    original_text=original_text[:100] + "..."
                    if len(original_text) > 100
                    else original_text,
                    translated_text=translated_text[:100] + "..."
                    if len(translated_text) > 100
                    else translated_text,
                    target_language=target_language,
                    detected_language=detected_language,
                )
            )

        return TranslationResponse(
            success=True,
            document_id=request.document_id,
            results=results,
            timestamp=request.timestamp,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        return TranslationResponse(
            success=False,
            document_id=request.document_id,
            results=[],
            error=f"AWS Translate {error_code}: {error_message}",
            timestamp=request.timestamp,
        )
    except Exception as e:
        return TranslationResponse(
            success=False,
            document_id=request.document_id,
            results=[],
            error=f"Unexpected error: {str(e)}",
            timestamp=request.timestamp,
        )


# Batch translation function
def translate_documents_batch(
    documents: List[Dict[str, Any]],
    field_mapping: Dict[str, str],  # field_name -> target_language
) -> Dict[str, Dict[str, str]]:
    """
    Translate specific fields in multiple documents.
    Returns dict: document_id -> {field_name: translated_text}
    """
    translations = {}

    for doc in documents:
        doc_id = doc.get("id", "unknown")
        request = TranslationRequest(
            document_id=doc_id, translations=field_mapping, document_data=doc
        )

        response = translate_record_fields(request)
        if response.success:
            doc_translations = {}
            for result in response.results:
                doc_translations[result.field_name] = result.translated_text
            translations[doc_id] = doc_translations

    return translations


# Language detection function
def detect_language(text: str) -> str:
    """
    Detect the language of a text using AWS Translate.
    """
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS credentials required")

    try:
        translate = get_translate_client()

        # Truncate if too long
        if len(text) > 5000:
            text = text[:5000]

        response = translate.translate_text(
            Text=text,
            SourceLanguageCode="auto",
            TargetLanguageCode="en",  # Translate to English to get detection
        )

        return response.get("SourceLanguageCode", "unknown")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        raise Exception(
            f"AWS Translate language detection failed: {error_code} - {error_message}"
        )
    except Exception as e:
        raise Exception(f"Language detection failed: {str(e)}")


# Supported languages helper
def get_supported_languages() -> List[Dict[str, str]]:
    """
    Get list of languages supported by AWS Translate.
    """
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS credentials required")

    try:
        translate = get_translate_client()
        response = translate.list_languages()

        languages = []
        for lang in response["Languages"]:
            languages.append(
                {
                    "code": lang["LanguageCode"],
                    "name": lang.get("LanguageName", lang["LanguageCode"]),
                }
            )

        return languages

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        raise Exception(
            f"Failed to get supported languages: {error_code} - {error_message}"
        )
    except Exception as e:
        raise Exception(f"Failed to get supported languages: {str(e)}")


# Helper for single field translation
def translate_single_field(
    text: str, target_language: str, source_language: str = "auto"
) -> str:
    """
    Translate a single text field.
    """
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS credentials required")

    try:
        translate = get_translate_client()

        # Truncate if too long
        if len(text) > 5000:
            text = text[:5000]

        response = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )

        return response["TranslatedText"]

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        raise Exception(f"Translation failed: {error_code} - {error_message}")
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")
