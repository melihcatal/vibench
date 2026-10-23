import os
from typing import Dict, Any, List, Optional
from google.cloud import translate_v2 as translate


def translate_invoice_notes(
    notes_text: str, target_language: str = "en"
) -> Dict[str, Any]:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not credentials_path:
        raise ValueError("Google Cloud credentials not configured")

    try:
        client = translate.Client()

        if not notes_text or not notes_text.strip():
            return {
                "original_text": notes_text,
                "translated_text": notes_text,
                "target_language": target_language,
                "detected_language": None,
                "confidence": None,
                "provider": "google_cloud_translation",
                "note": "Empty text, no translation needed",
            }

        result = client.translate(
            notes_text, target_language=target_language, format_="text"
        )

        return {
            "original_text": notes_text,
            "translated_text": result["translatedText"],
            "target_language": target_language,
            "detected_language": result.get("detectedSourceLanguage"),
            "confidence": None,
            "provider": "google_cloud_translation",
            "character_count": len(notes_text),
        }

    except Exception as e:
        return {
            "error": str(e),
            "original_text": notes_text,
            "target_language": target_language,
            "provider": "google_cloud_translation",
            "translation_failed": True,
        }


def translate_invoice_descriptions(
    invoice_data: Dict[str, Any], target_language: str = "en"
) -> Dict[str, Any]:
    translations = {
        "invoice_id": invoice_data.get("invoice_id"),
        "vendor": invoice_data.get("vendor"),
        "translations": {},
        "summary": {
            "total_items_translated": 0,
            "languages_detected": set(),
            "provider": "google_cloud_translation",
        },
    }

    fields_to_translate = [
        ("vendor_notes", invoice_data.get("vendor_notes")),
        ("invoice_description", invoice_data.get("description")),
        ("payment_terms", invoice_data.get("payment_terms")),
        ("shipping_notes", invoice_data.get("shipping_notes")),
    ]

    for field_name, field_value in fields_to_translate:
        if field_value and isinstance(field_value, str):
            translation_result = translate_invoice_notes(field_value, target_language)
            translations["translations"][field_name] = translation_result

            if not translation_result.get("translation_failed", False):
                translations["summary"]["total_items_translated"] += 1

                detected_lang = translation_result.get("detected_language")
                if detected_lang:
                    translations["summary"]["languages_detected"].add(detected_lang)

    line_items = invoice_data.get("line_items", [])
    if line_items:
        translations["line_item_translations"] = []

        for i, item in enumerate(line_items):
            item_translations = {
                "item_index": i,
                "original_description": item.get("description"),
                "translations": {},
            }

            description = item.get("description")
            if description and isinstance(description, str):
                translation_result = translate_invoice_notes(
                    description, target_language
                )
                item_translations["translations"]["description"] = translation_result

                if not translation_result.get("translation_failed", False):
                    translations["summary"]["total_items_translated"] += 1

                    detected_lang = translation_result.get("detected_language")
                    if detected_lang:
                        translations["summary"]["languages_detected"].add(detected_lang)

            translations["line_item_translations"].append(item_translations)

    translations["summary"]["languages_detected"] = list(
        translations["summary"]["languages_detected"]
    )

    return translations


def detect_invoice_language(invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not credentials_path:
        raise ValueError("Google Cloud credentials not configured")

    try:
        client = translate.Client()

        text_samples = []

        fields_to_check = [
            invoice_data.get("vendor_notes"),
            invoice_data.get("description"),
            invoice_data.get("payment_terms"),
        ]

        line_items = invoice_data.get("line_items", [])
        for item in line_items[:3]:
            description = item.get("description")
            if description:
                fields_to_check.append(description)

        valid_texts = [
            text
            for text in fields_to_check
            if text and isinstance(text, str) and text.strip()
        ]

        if not valid_texts:
            return {
                "invoice_id": invoice_data.get("invoice_id"),
                "detected_languages": [],
                "primary_language": None,
                "confidence": None,
                "provider": "google_cloud_translation",
                "note": "No text content available for language detection",
            }

        sample_text = valid_texts[0][:100]

        result = client.detect_language(sample_text)

        language_detection = {
            "invoice_id": invoice_data.get("invoice_id"),
            "detected_languages": [
                {
                    "language": result["language"],
                    "confidence": result.get("confidence"),
                    "sample_text": sample_text,
                }
            ],
            "primary_language": result["language"],
            "confidence": result.get("confidence"),
            "provider": "google_cloud_translation",
            "text_sample_count": len(valid_texts),
        }

        if len(valid_texts) > 1:
            additional_detections = []
            for text in valid_texts[1:4]:
                if text:
                    try:
                        det_result = client.detect_language(text[:100])
                        additional_detections.append(
                            {
                                "language": det_result["language"],
                                "confidence": det_result.get("confidence"),
                                "sample_source": "additional_text",
                            }
                        )
                    except:
                        continue

            if additional_detections:
                language_detection["additional_detections"] = additional_detections

                language_counts = {}
                for det in [
                    language_detection["detected_languages"][0]
                ] + additional_detections:
                    lang = det["language"]
                    language_counts[lang] = language_counts.get(lang, 0) + 1

                if language_counts:
                    primary_lang = max(language_counts.items(), key=lambda x: x[1])[0]
                    language_detection["primary_language"] = primary_lang

        return language_detection

    except Exception as e:
        return {
            "error": str(e),
            "invoice_id": invoice_data.get("invoice_id"),
            "provider": "google_cloud_translation",
            "detection_failed": True,
        }


def batch_translate_invoices(
    invoices_data: List[Dict[str, Any]], target_language: str = "en"
) -> Dict[str, Any]:
    batch_results = {
        "total_invoices": len(invoices_data),
        "successful_translations": 0,
        "failed_translations": 0,
        "total_text_items": 0,
        "languages_encountered": set(),
        "translations_by_invoice": {},
        "provider": "google_cloud_translation",
    }

    for invoice in invoices_data:
        invoice_id = invoice.get(
            "invoice_id", f"invoice_{len(batch_results['translations_by_invoice'])}"
        )

        try:
            translation_result = translate_invoice_descriptions(
                invoice, target_language
            )
            batch_results["translations_by_invoice"][invoice_id] = translation_result

            if not translation_result.get("error"):
                batch_results["successful_translations"] += 1

                total_items = translation_result.get("summary", {}).get(
                    "total_items_translated", 0
                )
                batch_results["total_text_items"] += total_items

                languages = translation_result.get("summary", {}).get(
                    "languages_detected", []
                )
                for lang in languages:
                    batch_results["languages_encountered"].add(lang)
            else:
                batch_results["failed_translations"] += 1

        except Exception as e:
            batch_results["translations_by_invoice"][invoice_id] = {
                "error": str(e),
                "translation_failed": True,
            }
            batch_results["failed_translations"] += 1

    batch_results["languages_encountered"] = list(
        batch_results["languages_encountered"]
    )

    return batch_results
