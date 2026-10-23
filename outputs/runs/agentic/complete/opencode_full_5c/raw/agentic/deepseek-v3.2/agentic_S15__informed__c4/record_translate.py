import os
from typing import Dict, Any, List
from google.cloud import translate_v2 as translate


def translate_text(
    text: str, target_language: str, source_language: str = None
) -> Dict[str, Any]:
    """
    Translate text using Google Cloud Translation.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Source language code (optional, auto-detected if None)

    Returns:
        dict: Translation result
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    try:
        client = translate.Client()

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
            "detected_source_language": result.get(
                "detectedSourceLanguage", source_language
            ),
            "target_language": target_language,
            "provider": "Google Cloud Translation",
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def translate_document_fields(
    document: Dict[str, Any],
    fields_to_translate: List[str],
    target_language: str,
    source_language: str = None,
) -> Dict[str, Any]:
    """
    Translate user-facing document fields.

    Args:
        document: Document containing fields to translate
        fields_to_translate: List of field names to translate
        target_language: Target language code
        source_language: Source language code (optional)

    Returns:
        dict: Translated document and translation details
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    translated_doc = document.copy()
    translation_results = {}

    try:
        client = translate.Client()

        for field in fields_to_translate:
            if field in document and isinstance(document[field], str):
                text = document[field]
                if text.strip():
                    if source_language:
                        result = client.translate(
                            text,
                            target_language=target_language,
                            source_language=source_language,
                        )
                    else:
                        result = client.translate(text, target_language=target_language)

                    translated_doc[field] = result["translatedText"]
                    translation_results[field] = {
                        "original": text,
                        "translated": result["translatedText"],
                        "detected_source_language": result.get(
                            "detectedSourceLanguage", source_language
                        ),
                    }

        return {
            "success": True,
            "translated_document": translated_doc,
            "translation_results": translation_results,
            "target_language": target_language,
            "fields_translated": list(translation_results.keys()),
            "provider": "Google Cloud Translation",
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def batch_translate_texts(
    texts: List[str], target_language: str, source_language: str = None
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
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    try:
        client = translate.Client()

        translations = []

        for text in texts:
            if not isinstance(text, str):
                translations.append(
                    {"original": text, "translated": None, "error": "Not a string"}
                )
                continue

            if source_language:
                result = client.translate(
                    text,
                    target_language=target_language,
                    source_language=source_language,
                )
            else:
                result = client.translate(text, target_language=target_language)

            translations.append(
                {
                    "original": text,
                    "translated": result["translatedText"],
                    "detected_source_language": result.get(
                        "detectedSourceLanguage", source_language
                    ),
                }
            )

        return {
            "success": True,
            "translations": translations,
            "target_language": target_language,
            "total_texts": len(texts),
            "successful_translations": len(
                [t for t in translations if t.get("translated")]
            ),
            "provider": "Google Cloud Translation",
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def detect_language(text: str) -> Dict[str, Any]:
    """
    Detect the language of text.

    Args:
        text: Text to analyze

    Returns:
        dict: Language detection result
    """
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    try:
        client = translate.Client()
        result = client.detect_language(text)

        return {
            "success": True,
            "text": text,
            "detected_language": result["language"],
            "confidence": result.get("confidence", 0.0),
            "provider": "Google Cloud Translation",
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
