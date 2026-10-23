import os
import json
from typing import Dict, Any, List, Optional
from google.cloud import translate_v2 as translate


def translate_text(
    text: str, target_language: str, source_language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translate text using Google Cloud Translation API.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Source language code (optional, auto-detected if not provided)

    Returns:
        dict: Translation result
    """
    try:
        # Google Cloud credentials from environment variable
        # GOOGLE_APPLICATION_CREDENTIALS should point to service account key file
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )

        # Initialize Google Cloud Translation client
        client = translate.Client()

        # Perform translation
        if source_language:
            result = client.translate(
                text, target_language=target_language, source_language=source_language
            )
        else:
            result = client.translate(text, target_language=target_language)

        return {
            "success": True,
            "original_text": text,
            "translated_text": result["translatedText"],
            "source_language": result.get("detectedSourceLanguage", source_language),
            "target_language": target_language,
            "provider": "Google Cloud Translation",
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Translation error: {str(e)}",
            "original_text": text[:100] + "..." if len(text) > 100 else text,
            "target_language": target_language,
        }


def translate_document_fields(
    document: Dict[str, Any],
    fields_to_translate: List[str],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate specific fields in a document.

    Args:
        document: Document containing fields to translate
        fields_to_translate: List of field names to translate
        target_language: Target language code
        source_language: Source language code (optional)

    Returns:
        dict: Translation results for all fields
    """
    try:
        translated_document = document.copy()
        translation_results = {}
        failed_fields = []

        for field_name in fields_to_translate:
            if field_name in document and isinstance(document[field_name], str):
                text = document[field_name]
                if text.strip():  # Only translate non-empty strings
                    result = translate_text(text, target_language, source_language)

                    if result["success"]:
                        translated_document[field_name] = result["translated_text"]
                        translation_results[field_name] = {
                            "success": True,
                            "original": text[:50] + "..." if len(text) > 50 else text,
                            "translated": result["translated_text"][:50] + "..."
                            if len(result["translated_text"]) > 50
                            else result["translated_text"],
                            "source_language": result["source_language"],
                        }
                    else:
                        translation_results[field_name] = {
                            "success": False,
                            "error": result.get("error", "Unknown error"),
                            "original": text[:50] + "..." if len(text) > 50 else text,
                        }
                        failed_fields.append(field_name)

        # Add translation metadata
        if "_translations" not in translated_document:
            translated_document["_translations"] = {}

        translated_document["_translations"][target_language] = {
            "translated_at": "timestamp_placeholder",  # In real implementation, use datetime
            "fields_translated": [
                f for f in fields_to_translate if f not in failed_fields
            ],
            "fields_failed": failed_fields,
            "source_language": source_language or "auto",
        }

        return {
            "success": True,
            "translated_document": translated_document,
            "translation_results": translation_results,
            "failed_fields": failed_fields,
            "document_id": document.get("_id", "unknown"),
            "target_language": target_language,
            "provider": "Google Cloud Translation",
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error translating document: {str(e)}",
            "document_id": document.get("_id", "unknown"),
            "target_language": target_language,
        }


def batch_translate_texts(
    texts: List[str], target_language: str, source_language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Translate multiple texts in batch.

    Args:
        texts: List of texts to translate
        target_language: Target language code
        source_language: Source language code (optional)

    Returns:
        dict: Batch translation results
    """
    try:
        # Google Cloud credentials from environment variable
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )

        # Initialize Google Cloud Translation client
        client = translate.Client()

        # Perform batch translation
        if source_language:
            results = client.translate(
                texts, target_language=target_language, source_language=source_language
            )
        else:
            results = client.translate(texts, target_language=target_language)

        translation_results = []
        for i, result in enumerate(results):
            translation_results.append(
                {
                    "text_index": i,
                    "original_text": texts[i][:50] + "..."
                    if len(texts[i]) > 50
                    else texts[i],
                    "translated_text": result["translatedText"],
                    "source_language": result.get(
                        "detectedSourceLanguage", source_language
                    ),
                    "success": True,
                }
            )

        return {
            "success": True,
            "total_texts": len(texts),
            "translated_texts": len(translation_results),
            "results": translation_results,
            "target_language": target_language,
            "provider": "Google Cloud Translation",
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Batch translation error: {str(e)}",
            "total_texts": len(texts),
            "target_language": target_language,
        }


def detect_language(text: str) -> Dict[str, Any]:
    """
    Detect the language of text using Google Cloud Translation API.

    Args:
        text: Text to detect language for

    Returns:
        dict: Language detection result
    """
    try:
        # Google Cloud credentials from environment variable
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )

        # Initialize Google Cloud Translation client
        client = translate.Client()

        # Detect language
        result = client.detect_language(text)

        return {
            "success": True,
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
            "detected_language": result["language"],
            "confidence": result.get("confidence", 0),
            "provider": "Google Cloud Translation",
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Language detection error: {str(e)}",
            "text_preview": text[:100] + "..." if len(text) > 100 else text,
        }
