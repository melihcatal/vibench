from __future__ import annotations

import os
from typing import Any, Dict

from openai import OpenAI

from document_models import NormalizedExpenseRecord


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Normalize the extracted expense document into a standard schema with keys: "
        "supplier_name, document_date, total_amount, tax_amount, currency, line_items, notes. "
        "Return strict JSON only."
    )
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": str(extracted)},
        ],
    )
    content = completion.choices[0].message.content
    normalized = __import__("json").loads(content)
    record = NormalizedExpenseRecord(
        record_type="expense",
        source_document_type=extracted.get("document_type", "unknown"),
        supplier_name=normalized.get("supplier_name") or extracted.get("vendor") or extracted.get("merchant"),
        document_date=normalized.get("document_date") or extracted.get("invoice_date"),
        total_amount=normalized.get("total_amount") or extracted.get("total"),
        tax_amount=normalized.get("tax_amount") or extracted.get("tax"),
        currency=normalized.get("currency") or extracted.get("currency"),
        line_items=normalized.get("line_items") or extracted.get("line_items") or extracted.get("items") or [],
        notes=normalized.get("notes") or extracted.get("notes"),
        validation={},
    )
    return record.to_dict()
