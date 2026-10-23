import os
from deep_translator import GoogleTranslator
from typing import Dict, Any, List, Optional


def record_translate(
    documents: List[Dict[str, Any]],
    target_language: str = "en",
    source_language: str = "auto",
    fields_to_translate: List[str] = None,
) -> Dict[str, Any]:
    """
    Translate user-facing document fields using Google Translate API.

    Args:
        documents: List of document records to translate
        target_language: Target language code (e.g., 'en', 'es', 'fr')
        source_language: Source language code or 'auto' for auto-detection
        fields_to_translate: Specific fields to translate (None for all text fields)

    Returns:
        dict: Translation results
    """
    try:
        # Initialize Google Translator
        translator = GoogleTranslator(source=source_language, target=target_language)

        results = []
        total_translations = 0
        failed_translations = 0

        for doc_idx, document in enumerate(documents):
            if not isinstance(document, dict):
                results.append(
                    {
                        "document_index": doc_idx,
                        "success": False,
                        "error": "Document is not a dictionary",
                        "translations": [],
                    }
                )
                continue

            doc_result = {
                "document_index": doc_idx,
                "document_id": document.get("id", f"doc_{doc_idx}"),
                "original_language": source_language
                if source_language != "auto"
                else "auto-detected",
                "target_language": target_language,
                "translations": [],
                "translated_fields": [],
            }

            # Determine which fields to translate
            fields = list(document.keys())
            if fields_to_translate:
                fields = [f for f in fields if f in fields_to_translate]

            for field_name in fields:
                field_value = document[field_name]

                # Only translate string fields
                if isinstance(field_value, str) and field_value.strip():
                    try:
                        # Translate the text
                        translated_text = translator.translate(field_value)

                        doc_result["translations"].append(
                            {
                                "field": field_name,
                                "original": field_value,
                                "translated": translated_text,
                                "success": True,
                            }
                        )

                        doc_result["translated_fields"].append(field_name)
                        total_translations += 1

                    except Exception as translate_error:
                        doc_result["translations"].append(
                            {
                                "field": field_name,
                                "original": field_value,
                                "error": str(translate_error),
                                "success": False,
                            }
                        )
                        failed_translations += 1
                else:
                    # Non-string field, skip translation
                    doc_result["translations"].append(
                        {
                            "field": field_name,
                            "original": field_value,
                            "note": "Not a translatable string field",
                            "success": True,
                        }
                    )

            results.append(doc_result)

        # Calculate success rate
        success_rate = (
            (total_translations / (total_translations + failed_translations) * 100)
            if (total_translations + failed_translations) > 0
            else 0
        )

        return {
            "success": True,
            "results": results,
            "summary": {
                "total_documents": len(documents),
                "total_translations_attempted": total_translations
                + failed_translations,
                "successful_translations": total_translations,
                "failed_translations": failed_translations,
                "success_rate": round(success_rate, 2),
                "target_language": target_language,
                "source_language": source_language,
            },
            "provider": "google:translate",
            "service": "deep_translator.GoogleTranslator",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "google:translate",
            "service": "deep_translator.GoogleTranslator",
        }


def translate_single_text(
    text: str, target_language: str = "en", source_language: str = "auto"
) -> Dict[str, Any]:
    """
    Translate a single text string using Google Translate.

    Args:
        text: Text to translate
        target_language: Target language code
        source_language: Source language code or 'auto'

    Returns:
        dict: Translation result
    """
    try:
        if not text or not text.strip():
            return {
                "success": True,
                "original": text,
                "translated": text,
                "note": "Empty text, no translation needed",
                "provider": "google:translate",
            }

        # Initialize translator
        translator = GoogleTranslator(source=source_language, target=target_language)

        # Translate the text
        translated_text = translator.translate(text)

        # Get detected language if auto-detection was used
        detected_language = None
        if source_language == "auto":
            # Note: deep_translator doesn't expose detected language directly
            # We'll use a simple workaround
            detected_language = "auto-detected"

        return {
            "success": True,
            "original": text,
            "translated": translated_text,
            "target_language": target_language,
            "source_language": source_language
            if source_language != "auto"
            else detected_language,
            "text_length": len(text),
            "translated_length": len(translated_text),
            "provider": "google:translate",
            "service": "deep_translator.GoogleTranslator",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "original": text,
            "provider": "google:translate",
            "service": "deep_translator.GoogleTranslator",
        }


def batch_translate_texts(
    texts: List[str], target_language: str = "en", source_language: str = "auto"
) -> Dict[str, Any]:
    """
    Translate multiple text strings in batch.

    Args:
        texts: List of text strings to translate
        target_language: Target language code
        source_language: Source language code

    Returns:
        dict: Batch translation results
    """
    try:
        translator = GoogleTranslator(source=source_language, target=target_language)

        results = []
        successful = 0
        failed = 0

        for i, text in enumerate(texts):
            try:
                if not text or not text.strip():
                    results.append(
                        {
                            "index": i,
                            "original": text,
                            "translated": text,
                            "success": True,
                            "note": "Empty text",
                        }
                    )
                    successful += 1
                else:
                    translated = translator.translate(text)
                    results.append(
                        {
                            "index": i,
                            "original": text,
                            "translated": translated,
                            "success": True,
                        }
                    )
                    successful += 1
            except Exception as e:
                results.append(
                    {"index": i, "original": text, "error": str(e), "success": False}
                )
                failed += 1

        return {
            "success": True,
            "results": results,
            "summary": {
                "total_texts": len(texts),
                "successful": successful,
                "failed": failed,
                "success_rate": round(successful / len(texts) * 100, 2) if texts else 0,
                "target_language": target_language,
                "source_language": source_language,
            },
            "provider": "google:translate",
            "service": "deep_translator.GoogleTranslator",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "google:translate",
            "service": "deep_translator.GoogleTranslator",
        }
