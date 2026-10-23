import os
from typing import Dict, List, Any, Optional
import json
from deep_translator import GoogleTranslator


def translate_invoice_notes(
    notes_text: str, target_language: str = "en"
) -> Dict[str, Any]:
    """
    Translate extracted invoice notes or descriptions using Google Translate API.
    """
    if not notes_text or not notes_text.strip():
        return {
            "original_text": notes_text,
            "translated_text": notes_text,
            "target_language": target_language,
            "source_language": "auto",
            "translation_provider": "google_translate",
            "character_count": 0,
            "translation_success": True,
        }

    try:
        translator = GoogleTranslator(source="auto", target=target_language)
        translated_text = translator.translate(notes_text)

        source_lang = translator.source
        if source_lang == target_language:
            source_lang = "auto_detected_same"

        result = {
            "original_text": notes_text,
            "translated_text": translated_text,
            "target_language": target_language,
            "source_language": source_lang,
            "translation_provider": "google_translate",
            "character_count": len(notes_text),
            "translation_success": True,
            "api_used": "deep_translator_google",
        }

    except Exception as e:
        result = {
            "original_text": notes_text,
            "translated_text": notes_text,
            "target_language": target_language,
            "source_language": "unknown",
            "translation_provider": "google_translate_fallback",
            "character_count": len(notes_text),
            "translation_success": False,
            "error": str(e),
            "api_used": "deep_translator_google",
        }

    return result


def translate_line_item_descriptions(
    line_items: List[Dict[str, Any]], target_language: str = "en"
) -> List[Dict[str, Any]]:
    """
    Translate descriptions in line items.
    """
    translated_items = []

    for item in line_items:
        translated_item = item.copy()

        if "description" in item and item["description"]:
            translation_result = translate_invoice_notes(
                item["description"], target_language
            )

            translated_item["original_description"] = item["description"]
            translated_item["description"] = translation_result["translated_text"]
            translated_item["translation_metadata"] = {
                "source_language": translation_result["source_language"],
                "target_language": translation_result["target_language"],
                "success": translation_result["translation_success"],
            }

        translated_items.append(translated_item)

    return translated_items


def translate_vendor_notes(
    invoice_data: Dict[str, Any], target_language: str = "en"
) -> Dict[str, Any]:
    """
    Translate all text fields in invoice data.
    """
    translated_data = invoice_data.copy()

    if "vendor" in invoice_data and invoice_data["vendor"]:
        vendor_translation = translate_invoice_notes(
            invoice_data["vendor"], target_language
        )
        translated_data["vendor"] = vendor_translation["translated_text"]
        translated_data["vendor_translation"] = vendor_translation

    if "notes" in invoice_data and invoice_data["notes"]:
        notes_translation = translate_invoice_notes(
            invoice_data["notes"], target_language
        )
        translated_data["notes"] = notes_translation["translated_text"]
        translated_data["notes_translation"] = notes_translation

    if "line_items" in invoice_data:
        translated_data["line_items"] = translate_line_item_descriptions(
            invoice_data["line_items"], target_language
        )

    translated_data["translation_target"] = target_language
    translated_data["translation_provider"] = "google_translate"

    return translated_data
