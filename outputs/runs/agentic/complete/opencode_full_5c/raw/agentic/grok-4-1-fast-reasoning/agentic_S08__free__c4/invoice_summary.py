from document_client import get_gemini_model
from document_models import NormalizedExpense
import json


def generate_invoice_summary(normalized: NormalizedExpense) -> str:
    if normalized.document_type != "invoice":
        raise ValueError("Only for invoices")
    model = get_gemini_model()
    prompt = f"""Provide a concise 1-2 sentence summary of this invoice:

{normalized.model_dump_json()}"""
    response = model.generate_content(prompt)
    return response.text.strip()
