import json
from typing import Dict, List, Any, Optional
from document_models import ExpenseRecord


def translate_invoice_notes(notes: str, target_language: str = "en") -> Dict[str, Any]:
    """
    Translate extracted invoice notes or descriptions using DeepL API.
    """
    import deepl

    auth_key = os.getenv("DEEPL_API_KEY")

    if not auth_key:
        return {
            "translated": False,
            "error": "DeepL API key not configured",
            "original_text": notes,
            "translated_text": notes,
            "target_language": target_language,
        }

    translator = deepl.Translator(auth_key)

    try:
        # Detect source language if not specified
        if not notes or not notes.strip():
            return {
                "translated": False,
                "error": "No text to translate",
                "original_text": notes,
                "translated_text": notes,
                "target_language": target_language,
            }

        # Translate the text
        result = translator.translate_text(notes, target_lang=target_language.upper())

        # Get detected source language
        detected_source_lang = (
            result.detected_source_lang.lower()
            if result.detected_source_lang
            else "unknown"
        )

        translation_result = {
            "translated": True,
            "original_text": notes,
            "translated_text": result.text,
            "source_language": detected_source_lang,
            "target_language": target_language,
            "character_count": len(notes),
            "translation_timestamp": datetime.utcnow().isoformat(),
            "api_used": "deepl",
            "model_used": "deepl_translator",
        }

        return translation_result

    except deepl.DeepLException as e:
        return {
            "translated": False,
            "error": f"DeepL API error: {str(e)}",
            "original_text": notes,
            "translated_text": notes,
            "target_language": target_language,
            "translation_timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "translated": False,
            "error": f"Unexpected error: {str(e)}",
            "original_text": notes,
            "translated_text": notes,
            "target_language": target_language,
            "translation_timestamp": datetime.utcnow().isoformat(),
        }


def translate_expense_descriptions(
    expense_record: ExpenseRecord, target_language: str = "en"
) -> Dict[str, Any]:
    """
    Translate all text descriptions in an expense record.
    """
    translation_results = {
        "vendor_translation": None,
        "item_translations": [],
        "metadata_translation": None,
        "overall_translation_summary": {},
    }

    # Translate vendor name if it appears to be in another language
    vendor_translation = translate_invoice_notes(
        expense_record.vendor_name, target_language
    )
    translation_results["vendor_translation"] = vendor_translation

    # Translate line item descriptions
    for i, item in enumerate(expense_record.line_items):
        description = item.get("description", "")
        if description:
            item_translation = translate_invoice_notes(description, target_language)
            translation_results["item_translations"].append(
                {
                    "item_index": i,
                    "original_description": description,
                    "translation_result": item_translation,
                }
            )

    # Translate metadata notes if present
    if expense_record.metadata and "notes" in expense_record.metadata:
        notes = expense_record.metadata["notes"]
        metadata_translation = translate_invoice_notes(notes, target_language)
        translation_results["metadata_translation"] = metadata_translation

    # Calculate translation statistics
    total_items = len(translation_results["item_translations"])
    successful_translations = sum(
        1
        for item in translation_results["item_translations"]
        if item["translation_result"].get("translated", False)
    )

    if vendor_translation.get("translated", False):
        successful_translations += 1

    if translation_results["metadata_translation"] and translation_results[
        "metadata_translation"
    ].get("translated", False):
        successful_translations += 1

    translation_results["overall_translation_summary"] = {
        "total_text_elements": total_items
        + 1
        + (1 if translation_results["metadata_translation"] else 0),
        "successful_translations": successful_translations,
        "success_rate": (
            successful_translations
            / (
                total_items
                + 1
                + (1 if translation_results["metadata_translation"] else 0)
            )
        )
        * 100
        if (total_items + 1 + (1 if translation_results["metadata_translation"] else 0))
        > 0
        else 0,
        "target_language": target_language,
        "source_languages_detected": list(
            set(
                [
                    result.get("source_language", "unknown")
                    for result in [
                        vendor_translation,
                        *[
                            item["translation_result"]
                            for item in translation_results["item_translations"]
                        ],
                        translation_results["metadata_translation"]
                        if translation_results["metadata_translation"]
                        else {},
                    ]
                    if result.get("translated", False)
                ]
            )
        ),
        "summary_timestamp": datetime.utcnow().isoformat(),
    }

    return translation_results


def batch_translate_notes(
    notes_list: List[str], target_language: str = "en"
) -> List[Dict[str, Any]]:
    """
    Translate multiple notes in batch.
    """
    results = []

    for notes in notes_list:
        result = translate_invoice_notes(notes, target_language)
        results.append(result)

    return results


def detect_language(text: str) -> Dict[str, Any]:
    """
    Detect the language of text using DeepL's language detection.
    """
    import deepl

    auth_key = os.getenv("DEEPL_API_KEY")

    if not auth_key:
        return {
            "detected": False,
            "error": "DeepL API key not configured",
            "text": text,
            "detected_language": "unknown",
        }

    translator = deepl.Translator(auth_key)

    try:
        # Use translation with source language detection
        result = translator.translate_text(
            text[:500],  # Limit text for detection
            target_lang="EN",  # Target doesn't matter for detection
        )

        return {
            "detected": True,
            "text_sample": text[:500],
            "detected_language": result.detected_source_lang.lower()
            if result.detected_source_lang
            else "unknown",
            "confidence": "high",  # DeepL doesn't provide confidence scores
            "detection_timestamp": datetime.utcnow().isoformat(),
            "api_used": "deepl",
        }

    except Exception as e:
        return {
            "detected": False,
            "error": str(e),
            "text": text,
            "detected_language": "unknown",
            "detection_timestamp": datetime.utcnow().isoformat(),
        }


if __name__ == "__main__":
    # Example usage
    from document_models import ExpenseRecord

    sample_record = ExpenseRecord(
        vendor_name="Fournitures de Bureau SA",
        transaction_date="2024-01-15",
        total_amount=1250.75,
        currency="EUR",
        line_items=[
            {
                "description": "Chaise de bureau ergonomique",
                "quantity": 2,
                "unit_price": 250,
                "amount": 500,
            },
            {
                "description": "Lampe de bureau LED",
                "quantity": 3,
                "unit_price": 83.58,
                "amount": 250.75,
            },
        ],
        metadata={"notes": "Facture pour fournitures de bureau du premier trimestre."},
    )

    translation_result = translate_expense_descriptions(sample_record, "en")
    print(json.dumps(translation_result, indent=2))
