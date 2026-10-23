import os
from typing import List, Optional

import deepl
from document_models import InvoiceExtractionResult

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_TARGET_LANGUAGE = os.environ.get("DEEPL_TARGET_LANGUAGE", "EN")


def translate_invoice_note(
    text: str,
    target_lang: Optional[str] = None,
    source_lang: Optional[str] = None,
) -> str:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(DEEPL_AUTH_KEY)
    target = target_lang or DEEPL_TARGET_LANGUAGE

    kwargs = {}
    if source_lang:
        kwargs["source_lang"] = source_lang

    result = translator.translate_text(text, target_lang=target, **kwargs)
    return result.text


def translate_invoice_notes(
    invoice_result: InvoiceExtractionResult,
    target_lang: Optional[str] = None,
    source_lang: Optional[str] = None,
) -> str:
    notes = invoice_result.notes or ""
    if not notes.strip():
        return ""
    return translate_invoice_note(
        notes, target_lang=target_lang, source_lang=source_lang
    )


def translate_line_item_descriptions(
    invoice_result: InvoiceExtractionResult,
    target_lang: Optional[str] = None,
    source_lang: Optional[str] = None,
) -> List[str]:
    translations = []
    for item in invoice_result.line_items:
        if item.description:
            translated = translate_invoice_note(
                item.description, target_lang=target_lang, source_lang=source_lang
            )
            translations.append(translated)
        else:
            translations.append("")
    return translations


def translate_vendor_address(
    invoice_result: InvoiceExtractionResult,
    target_lang: Optional[str] = None,
    source_lang: Optional[str] = None,
) -> str:
    address = invoice_result.vendor_address or ""
    if not address.strip():
        return ""
    return translate_invoice_note(
        address, target_lang=target_lang, source_lang=source_lang
    )


def translate_full_invoice_context(
    invoice_result: InvoiceExtractionResult,
    target_lang: Optional[str] = None,
    source_lang: Optional[str] = None,
) -> dict:
    translated_notes = translate_invoice_notes(
        invoice_result, target_lang=target_lang, source_lang=source_lang
    )
    translated_items = translate_line_item_descriptions(
        invoice_result, target_lang=target_lang, source_lang=source_lang
    )
    translated_address = translate_vendor_address(
        invoice_result, target_lang=target_lang, source_lang=source_lang
    )

    return {
        "original_vendor": invoice_result.vendor_name,
        "original_notes": invoice_result.notes,
        "translated_notes": translated_notes,
        "translated_address": translated_address,
        "translated_line_items": [
            {"original": item.description, "translated": trans}
            for item, trans in zip(invoice_result.line_items, translated_items)
        ],
        "target_language": target_lang or DEEPL_TARGET_LANGUAGE,
    }
