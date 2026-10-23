from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from document_client import get_openai_client
from document_models import NormalizedExpenseRecord


OPENAI_MODEL = "gpt-4.1-mini"


def normalize_expense(extracted_document: Dict[str, Any]) -> Dict[str, Any]:
    client: OpenAI = get_openai_client()
    prompt = (
        "Normalize the provided invoice or receipt extraction into a strict expense JSON object with keys: "
        "supplier_name, transaction_date, total_amount, tax_amount, currency, line_items, source_document_type, source_notes. "
        "Return only valid JSON."
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You normalize accounting documents."},
            {"role": "user", "content": f"{prompt}\nDocument:\n{extracted_document}"},
        ],
    )
    content = response.choices[0].message.content
    import json

    parsed = json.loads(content)
    record = NormalizedExpenseRecord(
        record_type="expense",
        supplier_name=parsed.get("supplier_name") or extracted_document.get("vendor") or extracted_document.get("merchant"),
        transaction_date=parsed.get("transaction_date") or extracted_document.get("invoice_date"),
        total_amount=parsed.get("total" if "total" in parsed else "total_amount") or extracted_document.get("total"),
        tax_amount=parsed.get("tax_amount") or extracted_document.get("tax"),
        currency=parsed.get("currency") or extracted_document.get("currency"),
        line_items=parsed.get("line_items") or extracted_document.get("items") or [],
        source_document_type=parsed.get("source_document_type") or extracted_document.get("document_type", "unknown"),
        source_notes=parsed.get("source_notes") or extracted_document.get("notes"),
    )
    return record.to_dict()
