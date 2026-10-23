"""Translate extracted invoice notes or descriptions using DeepL Translation API."""

import os
import json
import deepl
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TranslationResult:
    """Result of invoice note translation."""
    source_text: str = ""
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    detected_language: str = ""
    provider: str = "deepl_translation"
    model: str = "deepl_neural_mt"

    def to_dict(self) -> dict:
        return {
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "detected_language": self.detected_language,
            "provider": self.provider,
            "model": self.model,
        }


def translate_invoice_note(
    text: str,
    target_language: str = "EN-US",
    source_language: Optional[str] = None,
) -> TranslationResult:
    """Translate extracted invoice notes or descriptions using DeepL Translation API.

    Uses the DeepL API (api.deepl.com) with neural machine translation to translate
    vendor notes, memo fields, or line item descriptions.
    """
    api_key = os.environ.get("DEEPL_API_KEY", "")
    translator = deepl.Translator(api_key)

    translate_options = {
        "target_lang": target_language,
    }
    if source_language:
        translate_options["source_lang"] = source_language

    try:
        result = translator.translate_text(text, **translate_options)
    except deepl.DeepLException as exc:
        raise RuntimeError(f"DeepL Translation API call failed: {exc}") from exc

    return TranslationResult(
        source_text=text,
        translated_text=result.text,
        source_language=source_language or result.detected_source_lang or "",
        target_language=target_language,
        detected_language=result.detected_source_lang or "",
        provider="deepl_translation",
        model="deepl_neural_mt",
    )


def translate_line_item_descriptions(
    descriptions: list[str],
    target_language: str = "EN-US",
) -> list[TranslationResult]:
    """Translate multiple line item descriptions using DeepL batch translation."""
    api_key = os.environ.get("DEEPL_API_KEY", "")
    translator = deepl.Translator(api_key)

    if not descriptions:
        return []

    try:
        results = translator.translate_text(
            descriptions,
            target_lang=target_language,
        )
    except deepl.DeepLException as exc:
        raise RuntimeError(f"DeepL Translation API batch call failed: {exc}") from exc

    translated_results = []
    for orig, translated in zip(descriptions, results):
        translated_results.append(
            TranslationResult(
                source_text=orig,
                translated_text=translated.text,
                source_language=translated.detected_source_lang or "",
                target_language=target_language,
                detected_language=translated.detected_source_lang or "",
                provider="deepl_translation",
                model="deepl_neural_mt",
            )
        )

    return translated_results


def translate_invoice_notes(
    invoice_data: dict,
    target_language: str = "EN-US",
) -> dict:
    """Translate all text fields in an extracted invoice using DeepL Translation API.

    Translates vendor name, memo/notes, and line item descriptions.
    Uses api.deepl.com with DeepL neural MT engine.
    """
    api_key = os.environ.get("DEEPL_API_KEY", "")
    translator = deepl.Translator(api_key)

    translated_data = dict(invoice_data)
    translations_performed = {}

    text_fields = ["vendor", "invoice_notes", "memo", "description"]
    for field_name in text_fields:
        value = invoice_data.get(field_name)
        if value and isinstance(value, str) and value.strip():
            try:
                result = translator.translate_text(value, target_lang=target_language)
                translated_data[field_name] = result.text
                translations_performed[field_name] = {
                    "original": value,
                    "translated": result.text,
                    "detected_source": result.detected_source_lang,
                }
            except deepl.DeepLException:
                translated_data[field_name] = value

    line_items = invoice_data.get("line_items", [])
    translated_items = []
    for item in line_items:
        translated_item = dict(item)
        desc = item.get("description", "")
        if desc and isinstance(desc, str) and desc.strip():
            try:
                result = translator.translate_text(desc, target_lang=target_language)
                translated_item["description"] = result.text
                translated_item["description_translated_from"] = desc
            except deepl.DeepLException:
                pass
        translated_items.append(translated_item)

    translated_data["line_items"] = translated_items
    translated_data["_translations"] = translations_performed
    translated_data["_translation_provider"] = "deepl_translation"
    translated_data["_translation_endpoint"] = "api.deepl.com"

    return translated_data


if __name__ == "__main__":
    result = translate_invoice_note(
        text="Lieferung von Büromaterial gemäß Vertrag Nr. 2024-0892",
        target_language="EN-US",
    )
    print(json.dumps(result.to_dict(), indent=2))
