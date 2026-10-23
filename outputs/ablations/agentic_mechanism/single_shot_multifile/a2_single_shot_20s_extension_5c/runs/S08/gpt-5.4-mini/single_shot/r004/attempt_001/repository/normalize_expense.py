from typing import Any, Dict
from document_models import normalize_expense_record
from document_client import get_openai_client, get_normalization_model

MODEL_ID = get_normalization_model()


def normalize_expense(extracted_fields: Dict[str, Any]) -> Dict[str, Any]:
    client = get_openai_client()
    prompt = (
        "Normalize this expense extraction into a standard JSON schema with keys: "
        "source_type, vendor, merchant, transaction_date, subtotal, tax, total, currency, line_items, notes. "
        "Preserve confidence fields where present and return only valid JSON.\n\n"
        f"Input JSON:\n{extracted_fields}"
    )
    response = client.responses.create(
        model=MODEL_ID,
        input=prompt,
        temperature=0,
    )
    normalized = normalize_expense_record(response.output_text, extracted_fields)
    return normalized
