import os
from typing import Dict, Any, List
import json


def record_translate(
    documents: List[Dict[str, Any]],
    target_language: str = "en",
    source_language: str = "auto",
    fields_to_translate: List[str] = None,
) -> Dict[str, Any]:
    """
    Translate user-facing document fields using Google Cloud Translation API.

    Args:
        documents: List of document records
        target_language: Target language code (e.g., "en", "es", "fr")
        source_language: Source language code or "auto" for auto-detection
        fields_to_translate: Specific fields to translate (None for all text fields)

    Returns:
        dict: Translation results
    """
    try:
        from google.cloud import translate_v2 as translate

        # Initialize Google Cloud Translation client
        client = translate.Client()

        # Prepare text for translation
        translation_requests = []
        document_map = []

        for i, doc in enumerate(documents):
            doc_data = doc.get("data", {})
            doc_id = doc.get("id", f"doc_{i}")

            # Extract fields to translate
            fields_to_process = fields_to_translate or list(doc_data.keys())

            for field_name in fields_to_process:
                if field_name in doc_data:
                    value = doc_data[field_name]

                    # Only translate string values
                    if isinstance(value, str) and value.strip():
                        # Skip if already in target language (simple check)
                        if len(value) > 20:  # Only check longer texts
                            translation_requests.append(
                                {
                                    "text": value,
                                    "field": field_name,
                                    "document_id": doc_id,
                                }
                            )

                        document_map.append(
                            {
                                "document_id": doc_id,
                                "field": field_name,
                                "original_text": value[:100] + "..."
                                if len(value) > 100
                                else value,
                                "text_length": len(value),
                            }
                        )

        if not translation_requests:
            return {
                "success": False,
                "error": "No translatable text content found in specified fields",
                "provider": "google:translate",
            }

        # Batch translations (Google Translate API handles batching)
        translations = []

        for request in translation_requests:
            try:
                # Translate text
                result = client.translate(
                    request["text"],
                    target_language=target_language,
                    source_language=source_language
                    if source_language != "auto"
                    else None,
                    format_="text",
                )

                translations.append(
                    {
                        "document_id": request["document_id"],
                        "field": request["field"],
                        "original_text": request["text"][:150] + "..."
                        if len(request["text"]) > 150
                        else request["text"],
                        "translated_text": result["translatedText"],
                        "detected_language": result.get(
                            "detectedSourceLanguage",
                            source_language if source_language != "auto" else "unknown",
                        ),
                        "provider": "google:translate",
                    }
                )

            except Exception as e:
                translations.append(
                    {
                        "document_id": request["document_id"],
                        "field": request["field"],
                        "original_text": request["text"][:150] + "..."
                        if len(request["text"]) > 150
                        else request["text"],
                        "error": str(e),
                        "provider": "google:translate",
                    }
                )

        # Group translations by document
        translations_by_doc = {}
        for trans in translations:
            doc_id = trans["document_id"]
            if doc_id not in translations_by_doc:
                translations_by_doc[doc_id] = []
            translations_by_doc[doc_id].append(trans)

        # Create translated documents
        translated_documents = []

        for doc in documents:
            doc_id = doc.get("id")
            if doc_id in translations_by_doc:
                # Create translated version
                translated_doc = doc.copy()
                translated_data = translated_doc.get("data", {}).copy()

                # Apply translations
                doc_translations = translations_by_doc[doc_id]
                for trans in doc_translations:
                    if "translated_text" in trans:
                        field_name = trans["field"]
                        if field_name in translated_data:
                            # Create translated field with suffix
                            translated_field_name = f"{field_name}_{target_language}"
                            translated_data[translated_field_name] = trans[
                                "translated_text"
                            ]

                # Add translation metadata
                translated_data["_translation_metadata"] = {
                    "target_language": target_language,
                    "translated_fields": [
                        t["field"] for t in doc_translations if "translated_text" in t
                    ],
                    "translation_provider": "google:translate",
                }

                translated_doc["data"] = translated_data
                translated_documents.append(translated_doc)

        # Calculate statistics
        successful_translations = [t for t in translations if "translated_text" in t]
        failed_translations = [t for t in translations if "error" in t]

        # Detect most common source languages
        language_counts = {}
        for trans in successful_translations:
            lang = trans.get("detected_language", "unknown")
            language_counts[lang] = language_counts.get(lang, 0) + 1

        return {
            "success": True,
            "translations": translations,
            "translated_documents": translated_documents,
            "statistics": {
                "total_texts": len(translation_requests),
                "successful_translations": len(successful_translations),
                "failed_translations": len(failed_translations),
                "success_rate": (
                    len(successful_translations) / len(translation_requests) * 100
                )
                if translation_requests
                else 0,
                "target_language": target_language,
                "source_languages": language_counts,
            },
            "provider": "google:translate",
            "api_version": "v2",
        }

    except ImportError:
        return {
            "success": False,
            "error": "Google Cloud Translation library not installed. Install with: pip install google-cloud-translate",
            "provider": "google:translate",
        }
    except Exception as e:
        error_msg = str(e)
        if "credentials" in error_msg.lower():
            return {
                "success": False,
                "error": "Google Cloud credentials not configured. Set GOOGLE_APPLICATION_CREDENTIALS environment variable.",
                "provider": "google:translate",
            }
        return {
            "success": False,
            "error": f"Google Cloud Translation API error: {error_msg}",
            "provider": "google:translate",
        }
