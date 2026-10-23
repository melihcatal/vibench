import os
import json
from typing import Dict, Any, List
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential


def translate_text(
    text: str, target_language: str, source_language: str = None
) -> Dict[str, Any]:
    """
    Translate text using Azure AI Translator.

    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'es', 'fr', 'de')
        source_language: Source language code (optional, auto-detected if not provided)

    Returns:
        dict: Translation result
    """
    translator_key = os.getenv("AZURE_TRANSLATOR_KEY")
    translator_region = os.getenv("AZURE_TRANSLATOR_REGION")

    if not translator_key or not translator_region:
        return {
            "success": False,
            "error": "AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables are required",
            "translated_text": None,
        }

    if not text or not text.strip():
        return {
            "success": True,
            "translated_text": "",
            "original_text": "",
            "message": "Empty text requires no translation",
        }

    try:
        credential = AzureKeyCredential(translator_key)
        client = TextTranslationClient(
            endpoint=f"https://api.cognitive.microsofttranslator.com",
            credential=credential,
            region=translator_region,
        )

        input_text_elements = [InputTextItem(text=text)]

        if source_language:
            response = client.translate(
                content=input_text_elements,
                to=[target_language],
                from_parameter=source_language,
            )
        else:
            response = client.translate(
                content=input_text_elements, to=[target_language]
            )

        translation = response[0] if response else None

        if translation and translation.translations:
            translated_text = translation.translations[0].text
            detected_language = (
                translation.detected_language.language
                if translation.detected_language
                else source_language
            )

            return {
                "success": True,
                "translated_text": translated_text,
                "original_text": text,
                "source_language": detected_language,
                "target_language": target_language,
                "provider": "Azure AI Translator",
            }
        else:
            return {
                "success": False,
                "error": "No translation returned",
                "translated_text": None,
            }
    except Exception as e:
        return {"success": False, "error": str(e), "translated_text": None}


def translate_document_field(
    document: Dict[str, Any], field_name: str, target_language: str
) -> Dict[str, Any]:
    """
    Translate a specific field in a document.

    Args:
        document: Document containing the field to translate
        field_name: Name of the field to translate
        target_language: Target language code

    Returns:
        dict: Translation result with updated document
    """
    if field_name not in document:
        return {
            "success": False,
            "error": f"Field '{field_name}' not found in document",
            "document": document,
        }

    text_to_translate = document[field_name]

    if not isinstance(text_to_translate, str):
        return {
            "success": False,
            "error": f"Field '{field_name}' is not a string",
            "document": document,
        }

    translation_result = translate_text(text_to_translate, target_language)

    if translation_result["success"]:
        # Create translated field name
        translated_field = f"{field_name}_{target_language}"

        # Create copy of document with translated field
        translated_doc = document.copy()
        translated_doc[translated_field] = translation_result["translated_text"]
        translated_doc[f"{translated_field}_metadata"] = {
            "original_text": translation_result["original_text"],
            "source_language": translation_result.get("source_language"),
            "target_language": target_language,
            "provider": translation_result.get("provider"),
        }

        return {
            "success": True,
            "original_document": document,
            "translated_document": translated_doc,
            "translation_result": translation_result,
        }
    else:
        return {
            "success": False,
            "error": translation_result.get("error"),
            "document": document,
        }


def translate_multiple_fields(
    document: Dict[str, Any], field_mapping: Dict[str, str]
) -> Dict[str, Any]:
    """
    Translate multiple fields in a document to different languages.

    Args:
        document: Document containing fields to translate
        field_mapping: Dictionary mapping field names to target language codes

    Returns:
        dict: Translation results with updated document
    """
    translated_doc = document.copy()
    translation_results = {}
    errors = []

    for field_name, target_language in field_mapping.items():
        if field_name in document and isinstance(document[field_name], str):
            result = translate_text(document[field_name], target_language)
            translation_results[field_name] = result

            if result["success"]:
                translated_field = f"{field_name}_{target_language}"
                translated_doc[translated_field] = result["translated_text"]
                translated_doc[f"{translated_field}_metadata"] = {
                    "original_text": result["original_text"],
                    "source_language": result.get("source_language"),
                    "target_language": target_language,
                    "provider": result.get("provider"),
                }
            else:
                errors.append({"field": field_name, "error": result.get("error")})

    all_successful = len(errors) == 0

    return {
        "success": all_successful,
        "original_document": document,
        "translated_document": translated_doc,
        "translation_results": translation_results,
        "errors": errors if errors else None,
        "provider": "Azure AI Translator",
    }
