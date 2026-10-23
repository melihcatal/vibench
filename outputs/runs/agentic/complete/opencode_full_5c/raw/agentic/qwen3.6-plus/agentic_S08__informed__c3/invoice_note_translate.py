import os

import deepl

from document_models import InvoiceExtraction

DEEPL_TARGET_LANG = "EN"


def translate_invoice_note(
    text: str, target_lang: str = DEEPL_TARGET_LANG, source_lang: str = None
) -> str:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    translator = deepl.Translator(auth_key)
    kwargs = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang
    result = translator.translate_text(text, **kwargs)
    return result.text


def translate_invoice_notes(
    notes: list[str], target_lang: str = DEEPL_TARGET_LANG
) -> list[str]:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    translator = deepl.Translator(auth_key)
    if not notes:
        return []
    results = translator.translate_text(notes, target_lang=target_lang)
    if isinstance(results, list):
        return [r.text for r in results]
    return [results.text]


def translate_invoice_line_descriptions(
    invoice: InvoiceExtraction, target_lang: str = DEEPL_TARGET_LANG
) -> InvoiceExtraction:
    auth_key = os.environ.get("DEEPL_AUTH_KEY", "")
    translator = deepl.Translator(auth_key)
    descriptions = [
        item.description.value for item in invoice.line_items if item.description.value
    ]
    if descriptions:
        translated = translator.translate_text(descriptions, target_lang=target_lang)
        translated_texts = (
            [r.text for r in translated]
            if isinstance(translated, list)
            else [translated.text]
        )
        idx = 0
        for item in invoice.line_items:
            if item.description.value:
                item.description.value = translated_texts[idx]
                idx += 1
    return invoice


def translate_vendor_memo(
    invoice: InvoiceExtraction,
    memo_field: str = "vendor_name",
    target_lang: str = DEEPL_TARGET_LANG,
) -> str:
    text = getattr(invoice, memo_field, None)
    if text and hasattr(text, "value"):
        text = text.value
    if not text:
        return ""
    return translate_invoice_note(text, target_lang=target_lang)
