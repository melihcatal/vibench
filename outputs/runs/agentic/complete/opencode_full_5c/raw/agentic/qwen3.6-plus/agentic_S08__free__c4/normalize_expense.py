import os
import json
from typing import Dict, Any, Union
from openai import OpenAI
from document_client import get_openai_config
from document_models import (
    InvoiceExtraction,
    ReceiptExtraction,
    NormalizedExpense,
    normalize_invoice_to_expense,
    normalize_receipt_to_expense,
)


OPENAI_MODEL = "gpt-4o"
OPENAI_API_BASE = "https://api.openai.com/v1"


def normalize_expense_fields(
    extraction: Union[InvoiceExtraction, ReceiptExtraction],
    document_id: str,
    additional_context: Dict[str, Any] = None,
) -> NormalizedExpense:
    config = get_openai_config()
    api_key = config["api_key"]
    model = config.get("model", OPENAI_MODEL)
    api_base = config.get("api_base", OPENAI_API_BASE)

    client = OpenAI(api_key=api_key, base_url=api_base)

    if isinstance(extraction, InvoiceExtraction):
        base_normalized = normalize_invoice_to_expense(extraction, document_id)
    elif isinstance(extraction, ReceiptExtraction):
        base_normalized = normalize_receipt_to_expense(extraction, document_id)
    else:
        raise TypeError(f"Unsupported extraction type: {type(extraction)}")

    system_prompt = """You are an expense data normalization assistant. You receive extracted expense data and must normalize it into a strict JSON schema. Ensure all dates are ISO 8601 format, amounts are numeric, and currency codes are ISO 4217 three-letter codes. Fill in missing fields with sensible defaults or null where appropriate."""

    user_content = json.dumps(
        {
            "document_type": base_normalized.document_type,
            "vendor": base_normalized.vendor,
            "date": base_normalized.date,
            "total": base_normalized.total,
            "tax": base_normalized.tax,
            "currency": base_normalized.currency,
            "line_items": base_normalized.line_items,
            "source_document_id": base_normalized.source_document_id,
            "additional_context": additional_context or {},
        }
    )

    json_schema = {
        "type": "object",
        "properties": {
            "document_type": {"type": "string", "enum": ["invoice", "receipt"]},
            "vendor": {"type": "string"},
            "date": {"type": "string", "format": "date"},
            "total": {"type": "number", "minimum": 0},
            "tax": {"type": "number", "minimum": 0},
            "currency": {"type": "string", "pattern": "^[A-Z]{3}$"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "amount": {"type": "number"},
                    },
                },
            },
            "source_document_id": {"type": "string"},
            "normalized_at": {"type": "string", "format": "date-time"},
            "schema_version": {"type": "string"},
            "notes": {"type": "string"},
        },
        "required": [
            "document_type",
            "vendor",
            "date",
            "total",
            "currency",
            "source_document_id",
            "normalized_at",
            "schema_version",
        ],
    }

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "normalized_expense",
                "schema": json_schema,
                "strict": True,
            },
        },
    )

    normalized_data = json.loads(response.choices[0].message.content)

    return NormalizedExpense(
        document_type=normalized_data.get(
            "document_type", base_normalized.document_type
        ),
        vendor=normalized_data.get("vendor", base_normalized.vendor),
        date=normalized_data.get("date", base_normalized.date),
        total=normalized_data.get("total", base_normalized.total),
        tax=normalized_data.get("tax", base_normalized.tax),
        currency=normalized_data.get("currency", base_normalized.currency),
        line_items=normalized_data.get("line_items", base_normalized.line_items),
        source_document_id=normalized_data.get(
            "source_document_id", base_normalized.source_document_id
        ),
        normalized_at=normalized_data.get(
            "normalized_at", base_normalized.normalized_at
        ),
        schema_version=normalized_data.get(
            "schema_version", base_normalized.schema_version
        ),
    )


def normalize_expense_batch(
    extractions: list, document_ids: list, additional_context: Dict[str, Any] = None
) -> list:
    results = []
    for extraction, doc_id in zip(extractions, document_ids):
        normalized = normalize_expense_fields(extraction, doc_id, additional_context)
        results.append(normalized)
    return results


if __name__ == "__main__":
    from document_models import InvoiceExtraction, LineItem

    sample_invoice = InvoiceExtraction(
        vendor_name="Acme Supplies",
        invoice_date="2024-01-15",
        invoice_number="INV-2024-001",
        total_amount=1250.00,
        tax_amount=125.00,
        currency="USD",
        line_items=[
            LineItem(
                description="Office chairs", quantity=5, unit_price=200.0, total=1000.0
            )
        ],
    )
    result = normalize_expense_fields(sample_invoice, "doc-001")
    print(
        json.dumps(
            {
                "document_type": result.document_type,
                "vendor": result.vendor,
                "date": result.date,
                "total": result.total,
                "currency": result.currency,
            },
            indent=2,
        )
    )
