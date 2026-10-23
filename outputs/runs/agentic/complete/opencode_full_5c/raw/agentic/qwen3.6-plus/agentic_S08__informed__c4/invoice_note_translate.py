import os
import deepl
from document_models import NormalizedExpense


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")


def translate_invoice_notes(text: str, target_language: str = "EN-US") -> str:
    if not text or not text.strip():
        return ""

    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(text, target_lang=target_language)
    return result.text


def translate_line_item_descriptions(
    normalized_expense: NormalizedExpense, target_language: str = "EN-US"
) -> NormalizedExpense:
    translated_items = []
    for item in normalized_expense.line_items:
        if isinstance(item, dict):
            desc = item.get("description", "")
            if desc:
                item["description"] = translate_invoice_notes(desc, target_language)
            translated_items.append(item)
        else:
            translated_items.append(translate_invoice_notes(str(item), target_language))

    normalized_expense.line_items = translated_items
    return normalized_expense


def translate_vendor_memo(
    normalized_expense: NormalizedExpense, target_language: str = "EN-US"
) -> NormalizedExpense:
    if normalized_expense.vendor_or_merchant:
        normalized_expense.vendor_or_merchant = translate_invoice_notes(
            normalized_expense.vendor_or_merchant, target_language
        )
    return normalized_expense


def translate_expense_notes_from_dict(
    expense_dict: dict, target_language: str = "EN-US"
) -> dict:
    normalized = NormalizedExpense(
        document_type=expense_dict.get("document_type", ""),
        vendor_or_merchant=expense_dict.get("vendor_or_merchant", ""),
        date=expense_dict.get("date", ""),
        subtotal=expense_dict.get("subtotal", 0.0),
        tax=expense_dict.get("tax", 0.0),
        total=expense_dict.get("total", 0.0),
        line_items=expense_dict.get("line_items", []),
        currency=expense_dict.get("currency", "USD"),
        confidence=expense_dict.get("confidence", 0.0),
    )
    normalized = translate_line_item_descriptions(normalized, target_language)
    return normalized.to_dict()
