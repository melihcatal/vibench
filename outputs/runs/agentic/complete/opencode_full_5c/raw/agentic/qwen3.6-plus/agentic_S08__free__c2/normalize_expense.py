import json
import openai
from document_models import (
    InvoiceFields,
    ReceiptFields,
    ExpenseRecord,
    invoice_fields_to_expense_record,
    receipt_fields_to_expense_record,
)
from document_client import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    validate_openai_credentials,
    build_openai_structured_extraction_payload,
    parse_openai_json_response,
)

STANDARD_EXPENSE_SCHEMA = {
    "document_type": "string (invoice or receipt)",
    "vendor_or_merchant": "string",
    "date": "string (ISO 8601 format YYYY-MM-DD)",
    "total_amount": "number",
    "tax_amount": "number",
    "currency": "string (ISO 4217 code, e.g. USD)",
    "line_items": "array of {description, quantity, unit_price, total}",
    "confidence": "number (0.0 to 1.0)",
    "normalized_at": "string (ISO 8601 timestamp)",
    "record_id": "string (unique identifier)",
}


def normalize_expense_from_invoice(
    invoice: InvoiceFields,
    source_provider: str = "google_document_ai",
) -> ExpenseRecord:
    base_record = invoice_fields_to_expense_record(invoice, source_provider)
    normalized = _normalize_with_openai(base_record)
    return normalized


def normalize_expense_from_receipt(
    receipt: ReceiptFields,
    source_provider: str = "aws_textract",
) -> ExpenseRecord:
    base_record = receipt_fields_to_expense_record(receipt, source_provider)
    normalized = _normalize_with_openai(base_record)
    return normalized


def normalize_expense_from_raw_data(
    raw_data: dict,
    document_type: str = "expense",
) -> ExpenseRecord:
    if not validate_openai_credentials():
        raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY.")

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    schema_desc = json.dumps(STANDARD_EXPENSE_SCHEMA, indent=2)
    payload = build_openai_structured_extraction_payload(
        text_content=json.dumps(raw_data, indent=2),
        schema_description=schema_desc,
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=payload["messages"],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    parsed = parse_openai_json_response(response)

    return ExpenseRecord(
        document_type=parsed.get("document_type", document_type),
        vendor_or_merchant=parsed.get("vendor_or_merchant", ""),
        date=parsed.get("date", ""),
        total_amount=float(parsed.get("total_amount", 0.0)),
        tax_amount=float(parsed.get("tax_amount", 0.0)),
        currency=parsed.get("currency", "USD"),
        line_items=parsed.get("line_items", []),
        confidence=float(parsed.get("confidence", 0.0)),
        source_provider="openai_gpt4o_mini",
        normalized_at=parsed.get("normalized_at", ""),
        record_id=parsed.get("record_id", ""),
        metadata=parsed.get("metadata", {}),
    )


def _normalize_with_openai(record: ExpenseRecord) -> ExpenseRecord:
    if not validate_openai_credentials():
        raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY.")

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    schema_desc = json.dumps(STANDARD_EXPENSE_SCHEMA, indent=2)
    payload = build_openai_structured_extraction_payload(
        text_content=json.dumps(
            {
                "document_type": record.document_type,
                "vendor_or_merchant": record.vendor_or_merchant,
                "date": record.date,
                "total_amount": record.total_amount,
                "tax_amount": record.tax_amount,
                "currency": record.currency,
                "line_items": record.line_items,
            },
            indent=2,
        ),
        schema_description=schema_desc,
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=payload["messages"],
        response_format={"type": "json_object"},
        temperature=0.0,
    )

    parsed = parse_openai_json_response(response)

    return ExpenseRecord(
        document_type=parsed.get("document_type", record.document_type),
        vendor_or_merchant=parsed.get("vendor_or_merchant", record.vendor_or_merchant),
        date=parsed.get("date", record.date),
        total_amount=float(parsed.get("total_amount", record.total_amount)),
        tax_amount=float(parsed.get("tax_amount", record.tax_amount)),
        currency=parsed.get("currency", record.currency),
        line_items=parsed.get("line_items", record.line_items),
        confidence=float(parsed.get("confidence", record.confidence)),
        source_provider="openai_gpt4o_mini",
        normalized_at=parsed.get("normalized_at", record.normalized_at),
        record_id=parsed.get("record_id", record.record_id),
        metadata=parsed.get("metadata", record.metadata),
    )
