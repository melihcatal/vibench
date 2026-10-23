import os
from typing import Optional

from document_client import (
    get_textract_client,
    analyze_document_bytes,
    parse_key_value_blocks,
    parse_table_blocks,
)
from document_models import InvoiceExtraction, LineItem, ExtractedField


INVOICE_FIELD_MAPPING = {
    "Vendor Name": ["vendor", "Vendor", "Company Name", "Supplier", "From"],
    "Invoice Date": ["invoice_date", "Date", "Invoice Date", "Bill Date"],
    "Total": ["total_amount", "Total", "Amount Due", "Grand Total", "Balance Due"],
    "Tax": ["tax_amount", "Tax", "Tax Amount", "VAT", "Sales Tax"],
    "Currency": ["currency", "Currency"],
}


def extract_invoice_fields(image_bytes: bytes) -> InvoiceExtraction:
    client = get_textract_client()
    response = analyze_document_bytes(client, image_bytes)
    blocks = response.get("Blocks", [])

    kv_pairs = parse_key_value_blocks(blocks)
    tables = parse_table_blocks(blocks)

    raw_fields = {}
    vendor = ""
    invoice_date = ""
    total_amount = 0.0
    tax_amount = 0.0
    currency = "USD"

    for canonical_key, aliases in INVOICE_FIELD_MAPPING.items():
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
            if field_name == "vendor":
                vendor = value
            elif field_name == "invoice_date":
                invoice_date = value
            elif field_name == "total_amount":
                total_amount = _parse_float(value)
            elif field_name == "tax_amount":
                tax_amount = _parse_float(value)
            elif field_name == "currency":
                currency = value if value else "USD"

    line_items = _extract_line_items_from_tables(tables, kv_pairs)

    confidences = [f.confidence for f in raw_fields.values()]
    confidence_overall = sum(confidences) / len(confidences) if confidences else 0.0

    return InvoiceExtraction(
        vendor=vendor,
        invoice_date=invoice_date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        currency=currency,
        line_items=line_items,
        raw_fields=raw_fields,
        confidence_overall=confidence_overall,
    )


def _parse_float(value: str) -> float:
    cleaned = value.replace("$", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _extract_line_items_from_tables(tables, kv_pairs):
    line_items = []
    for table in tables:
        if not table:
            continue
        header_row = table[0] if table else []
        desc_idx = None
        qty_idx = None
        price_idx = None
        total_idx = None
        for i, col in enumerate(header_row):
            col_lower = col.lower()
            if "desc" in col_lower or "item" in col_lower:
                desc_idx = i
            elif "qty" in col_lower or "quantity" in col_lower:
                qty_idx = i
            elif "price" in col_lower or "rate" in col_lower or "unit" in col_lower:
                price_idx = i
            elif "total" in col_lower or "amount" in col_lower or "ext" in col_lower:
                total_idx = i

        if desc_idx is None:
            desc_idx = 0
        if total_idx is None:
            total_idx = len(header_row) - 1 if header_row else 0

        for row in table[1:]:
            if not row:
                continue
            description = row[desc_idx] if desc_idx < len(row) else ""
            quantity = (
                _parse_float(row[qty_idx])
                if qty_idx is not None and qty_idx < len(row)
                else 1.0
            )
            unit_price = (
                _parse_float(row[price_idx])
                if price_idx is not None and price_idx < len(row)
                else 0.0
            )
            total = _parse_float(row[total_idx]) if total_idx < len(row) else 0.0

            if description.strip():
                line_items.append(
                    LineItem(
                        description=description.strip(),
                        quantity=quantity,
                        unit_price=unit_price,
                        total=total,
                        confidence=0.85,
                    )
                )
    return line_items
