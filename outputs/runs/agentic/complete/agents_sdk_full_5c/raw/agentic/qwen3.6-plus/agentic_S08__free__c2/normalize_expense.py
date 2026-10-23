"""Normalizes extracted expense fields into a standard JSON schema using OpenAI for semantic field mapping and enrichment."""

import json
import os
from typing import Dict, Any, Optional, Union
from datetime import datetime

import openai
from openai import OpenAI

from document_models import (
    NormalizedExpense,
    InvoiceExtraction,
    ReceiptExtraction,
    LineItem
)


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"


def normalize_expense(
    extraction: Union[InvoiceExtraction, ReceiptExtraction],
    document_type: str = "invoice",
    api_key: str = OPENAI_API_KEY,
    model: str = OPENAI_MODEL
) -> NormalizedExpense:
    client = OpenAI(api_key=api_key)

    raw_fields = _build_raw_fields(extraction, document_type)

    prompt = (
        f"You are a document normalization assistant. "
        f"Given the following extracted {document_type} data, normalize it into "
        f"a standard expense record with consistent field names, currency codes, "
        f"and ISO 8601 dates.\n\n"
        f"Input data:\n{json.dumps(raw_fields, indent=2)}\n\n"
        f"Return ONLY a JSON object with these keys: "
        f"entity_name, transaction_date (ISO 8601), total_amount, tax_amount, "
        f"currency (3-letter ISO 4217), line_items (array of objects with description, quantity, unit_price, total), "
        f"and any metadata notes."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a structured data normalization engine. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        response_format={"type": "json_object"}
    )

    normalized_json = json.loads(response.choices[0].message.content)

    entity_name = normalized_json.get("entity_name", "")
    if not entity_name:
        entity_name = raw_fields.get("vendor", "") or raw_fields.get("merchant", "")

    transaction_date = normalized_json.get("transaction_date", "")
    if not transaction_date:
        transaction_date = raw_fields.get("date", "")

    total_amount = normalized_json.get("total_amount", 0.0)
    tax_amount = normalized_json.get("tax_amount", 0.0)
    currency = normalized_json.get("currency", "USD")

    line_items = []
    raw_items = normalized_json.get("line_items", [])
    for li in raw_items:
        line_items.append({
            "description": li.get("description", ""),
            "quantity": li.get("quantity"),
            "unit_price": li.get("unit_price"),
            "total": float(li.get("total", 0.0))
        })

    if isinstance(extraction, InvoiceExtraction):
        li_data = [item.model_dump() for item in extraction.line_items]
    elif isinstance(extraction, ReceiptExtraction):
        li_data = [item.model_dump() for item in extraction.items]
    else:
        li_data = []

    if not line_items:
        for li in li_data:
            line_items.append(li)

    metadata = {
        "original_document_type": document_type,
        "original_confidence": extraction.confidence,
        "normalization_model": model,
        "normalization_provider": "openai",
        "normalized_at": datetime.utcnow().isoformat(),
        "ai_metadata": normalized_json.get("metadata_notes", "")
    }

    return NormalizedExpense(
        entity_name=entity_name,
        document_type=document_type,
        transaction_date=transaction_date,
        total_amount=float(total_amount),
        tax_amount=float(tax_amount) if tax_amount else 0.0,
        currency=currency,
        line_items=line_items,
        metadata=metadata,
        validation_status="pending",
        created_at=datetime.utcnow().isoformat()
    )


def normalize_expense_batch(
    extractions: list,
    api_key: str = OPENAI_API_KEY,
    model: str = OPENAI_MODEL
) -> list:
    results = []
    for ext in extractions:
        doc_type = "invoice" if isinstance(ext, InvoiceExtraction) else "receipt"
        norm = normalize_expense(ext, document_type=doc_type, api_key=api_key, model=model)
        results.append(norm)
    return results


def _build_raw_fields(
    extraction: Union[InvoiceExtraction, ReceiptExtraction],
    document_type: str
) -> Dict[str, Any]:
    if isinstance(extraction, InvoiceExtraction):
        return {
            "vendor": extraction.vendor,
            "date": extraction.invoice_date,
            "total": extraction.total,
            "tax": extraction.tax,
            "line_items": [item.model_dump() for item in extraction.line_items],
            "confidence": extraction.confidence
        }
    elif isinstance(extraction, ReceiptExtraction):
        return {
            "merchant": extraction.merchant,
            "date": extraction.transaction_date,
            "total": extraction.total,
            "tax": extraction.tax,
            "line_items": [item.model_dump() for item in extraction.items],
            "confidence": extraction.confidence
        }
    return {}


if __name__ == "__main__":
    invoice = InvoiceExtraction(
        vendor="Acme Supplies Inc.",
        invoice_date="2024-11-15",
        total=1250.00,
        tax=125.00,
        line_items=[
            LineItem(description="Office chairs", quantity=5, unit_price=200.0, total=1000.0),
            LineItem(description="Desk lamps", quantity=10, unit_price=25.0, total=250.0)
        ],
        confidence=0.95
    )
    result = normalize_expense(invoice, document_type="invoice")
    print(json.dumps(result.model_dump(), indent=2, default=str))
