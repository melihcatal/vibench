import os
from typing import Optional

from document_client import (
    get_textract_client,
    analyze_document_bytes,
    parse_key_value_blocks,
    parse_table_blocks,
)
from document_models import ReceiptExtraction, ExtractedField


RECEIPT_FIELD_MAPPING = {
    "Merchant": ["merchant", "Merchant", "Store", "Shop", "Business Name", "Vendor"],
    "Date": ["receipt_date", "Date", "Transaction Date", "Receipt Date", "Time"],
    "Total": ["total_amount", "Total", "Grand Total", "Amount", "Total Amount"],
    "Tax": ["tax_amount", "Tax", "Tax Amount", "Sales Tax", "VAT", "GST"],
    "Currency": ["currency", "Currency"],
}


def extract_receipt_fields(image_bytes: bytes) -> ReceiptExtraction:
    client = get_textract_client()
    response = analyze_document_bytes(client, image_bytes)
    blocks = response.get("Blocks", [])

    kv_pairs = parse_key_value_blocks(blocks)
    tables = parse_table_blocks(blocks)

    raw_fields = {}
    merchant = ""
    receipt_date = ""
    total_amount = 0.0
    tax_amount = 0.0
    currency = "USD"

    for canonical_key, aliases in RECEIPT_FIELD_MAPPING.items():
        matched_key = None
        for alias in aliases:
            for k in kv_pairs:
                if k.lower() == alias.lower():
                    matched_key = k
                    break
            if matched_key:
                break
        if matched_key:
            entry = kv_pairs[matched_key]
            value = entry["value"]
            confidence = entry["confidence"]
            field_name = aliases[0]
            raw_fields[field_name] = ExtractedField(
                name=field_name, value=value, confidence=confidence
            )
            if field_name == "merchant":
                merchant = value
            elif field_name == "receipt_date":
                receipt_date = value
            elif field_name == "total_amount":
                total_amount = _parse_float(value)
            elif field_name == "tax_amount":
                tax_amount = _parse_float(value)
            elif field_name == "currency":
                currency = value if value else "USD"

    items = _extract_receipt_items(tables, kv_pairs)

    confidences = [f.confidence for f in raw_fields.values()]
    confidence_overall = sum(confidences) / len(confidences) if confidences else 0.0

    return ReceiptExtraction(
        merchant=merchant,
        receipt_date=receipt_date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        currency=currency,
        items=items,
        raw_fields=raw_fields,
        confidence_overall=confidence_overall,
    )


def _parse_float(value: str) -> float:
    cleaned = value.replace("$", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _extract_receipt_items(tables, kv_pairs):
    items = []
    for table in tables:
        if not table:
            continue
        header_row = table[0] if table else []
        desc_idx = None
        price_idx = None
        for i, col in enumerate(header_row):
            col_lower = col.lower()
            if "item" in col_lower or "desc" in col_lower or "product" in col_lower:
                desc_idx = i
            elif "price" in col_lower or "amount" in col_lower or "cost" in col_lower:
                price_idx = i

        if desc_idx is None:
            desc_idx = 0
        if price_idx is None:
            price_idx = 1 if len(header_row) > 1 else 0

        for row in table[1:]:
            if not row:
                continue
            description = row[desc_idx] if desc_idx < len(row) else ""
            price = _parse_float(row[price_idx]) if price_idx < len(row) else 0.0

            if description.strip():
                items.append(
                    {
                        "description": description.strip(),
                        "price": price,
                        "confidence": 0.85,
                    }
                )
    return items
