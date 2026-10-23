import os
import deepl
from document_models import InvoiceExtractionResult

DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")


def translate_invoice_note(
    text: str, target_lang: str = "EN-US", source_lang: str = None
) -> str:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY must be set for DeepL translation")

    translator = deepl.Translator(DEEPL_AUTH_KEY)

    kwargs = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    result = translator.translate_text(text, **kwargs)
    return result.text


def translate_invoice_notes_from_invoice(
    invoice_result: InvoiceExtractionResult, target_lang: str = "EN-US"
) -> dict:
    translations = {}

    vendor_name = (
        invoice_result.vendor_name.value
        if hasattr(invoice_result.vendor_name, "value")
        else ""
    )
    if vendor_name and vendor_name.strip():
        translations["vendor_name"] = translate_invoice_note(vendor_name, target_lang)

    billing_address = (
        invoice_result.billing_address.value
        if hasattr(invoice_result.billing_address, "value")
        else ""
    )
    if billing_address and billing_address.strip():
        translations["billing_address"] = translate_invoice_note(
            billing_address, target_lang
        )

    for idx, item in enumerate(invoice_result.line_items):
        if item.description and item.description.strip():
            translated = translate_invoice_note(item.description, target_lang)
            translations[f"line_item_{idx}_description"] = translated

    return translations


def translate_invoice_notes_from_dict(
    invoice_data: dict, target_lang: str = "EN-US"
) -> dict:
    translations = {}

    vendor_name = invoice_data.get("vendor_name", {}).get("value", "")
    if vendor_name and vendor_name.strip():
        translations["vendor_name"] = translate_invoice_note(vendor_name, target_lang)

    billing_address = invoice_data.get("billing_address", {}).get("value", "")
    if billing_address and billing_address.strip():
        translations["billing_address"] = translate_invoice_note(
            billing_address, target_lang
        )

    line_items = invoice_data.get("line_items", [])
    for idx, item in enumerate(line_items):
        description = item.get("description", "")
        if description and description.strip():
            translations[f"line_item_{idx}_description"] = translate_invoice_note(
                description, target_lang
            )

    return translations


def batch_translate_texts(
    texts: list, target_lang: str = "EN-US", source_lang: str = None
) -> list:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY must be set for DeepL translation")

    translator = deepl.Translator(DEEPL_AUTH_KEY)

    kwargs = {"target_lang": target_lang}
    if source_lang:
        kwargs["source_lang"] = source_lang

    filtered_texts = [t for t in texts if t and t.strip()]
    if not filtered_texts:
        return []

    results = translator.translate_text(filtered_texts, **kwargs)
    return [r.text for r in results]
