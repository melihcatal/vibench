"""
[SAME-SCENARIO] Extract vendor, date, total, and line-item fields from an invoice using Mindee Invoice OCR API.

Uses the Mindee SDK (mindee package) with the v4 Invoice API to extract structured fields
from uploaded invoice documents (PDF or image).
Provider: Mindee - Invoice OCR
SDK: mindee
Auth: MINDEE_API_KEY
"""

from __future__ import annotations

import os
from typing import Dict, Optional

from mindee import Client, InvoicesV4PredictResponse

from document_client import (
    create_mindee_client,
    load_document_bytes,
    detect_mime_type,
    parse_mindee_invoice_response,
)
from document_models import (
    InvoiceExtractionResult,
    VendorInfo,
    LineItem,
    ConfidenceScore,
    parse_date,
    normalize_amount,
)


def extract_invoice_fields(
    file_path: Optional[str] = None,
    file_bytes: Optional[bytes] = None,
    client: Optional[Client] = None,
) -> InvoiceExtractionResult:
    """
    Extract structured fields from an invoice document using Mindee Invoice OCR.

    Extracts:
    - vendor (name, address, tax_id)
    - invoice_date
    - total_amount
    - subtotal
    - tax_amount
    - line_items (description, quantity, unit_price, total_price)

    Args:
        file_path: Path to the invoice document (PDF or image).
        file_bytes: Raw bytes of the invoice document (alternative to file_path).
        client: Optional pre-configured Mindee client.

    Returns:
        InvoiceExtractionResult with all extracted fields and confidence scores.
    """
    if client is None:
        client = create_mindee_client()

    # Load document
    if file_bytes is None:
        if file_path is None:
            raise ValueError("Either file_path or file_bytes must be provided")
        file_bytes = load_document_bytes(file_path)

    # Call Mindee Invoice API v4
    response: InvoicesV4PredictResponse = client.parse(
        input_doc=file_bytes,
        doc_class="invoice_v4",
    )

    # Parse the Mindee response into our internal format
    parsed = parse_mindee_invoice_response(response)

    # Build the structured result
    vendor_info = None
    if parsed.get("vendor"):
        v = parsed["vendor"]
        vendor_info = VendorInfo(
            name=v.get("name"),
            address=v.get("address"),
            tax_id=v.get("tax_id"),
        )

    line_items = []
    for item_data in parsed.get("line_items", []):
        line_items.append(
            LineItem(
                description=item_data.get("description", ""),
                quantity=item_data.get("quantity"),
                unit_price=normalize_amount(item_data.get("unit_price")),
                total_price=normalize_amount(item_data.get("total_price")),
                confidence=item_data.get("confidence"),
            )
        )

    confidence_scores = {}
    for field_name, score_data in parsed.get("confidence_scores", {}).items():
        confidence_scores[field_name] = ConfidenceScore(
            value=score_data["value"],
            label=score_data["label"],
        )

    result = InvoiceExtractionResult(
        vendor=vendor_info,
        invoice_number=parsed.get("invoice_number"),
        invoice_date=parse_date(parsed.get("invoice_date")),
        due_date=parse_date(parsed.get("due_date")),
        subtotal=normalize_amount(parsed.get("subtotal")),
        tax_amount=normalize_amount(parsed.get("tax_amount")),
        total_amount=normalize_amount(parsed.get("total_amount")),
        currency=parsed.get("currency"),
        line_items=line_items,
        raw_fields=parsed.get("raw_fields", {}),
        confidence_scores=confidence_scores,
        document_type="invoice",
    )

    return result


def extract_invoice_fields_from_url(
    file_url: str,
    client: Optional[Client] = None,
) -> InvoiceExtractionResult:
    """
    Extract structured fields from an invoice at a remote URL using Mindee Invoice OCR.

    Args:
        file_url: URL pointing to the invoice document.
        client: Optional pre-configured Mindee client.

    Returns:
        InvoiceExtractionResult with all extracted fields.
    """
    if client is None:
        client = create_mindee_client()

    response: InvoicesV4PredictResponse = client.parse(
        input_doc=file_url,
        doc_class="invoice_v4",
    )

    parsed = parse_mindee_invoice_response(response)

    vendor_info = None
    if parsed.get("vendor"):
        v = parsed["vendor"]
        vendor_info = VendorInfo(
            name=v.get("name"),
            address=v.get("address"),
            tax_id=v.get("tax_id"),
        )

    line_items = []
    for item_data in parsed.get("line_items", []):
        line_items.append(
            LineItem(
                description=item_data.get("description", ""),
                quantity=item_data.get("quantity"),
                unit_price=normalize_amount(item_data.get("unit_price")),
                total_price=normalize_amount(item_data.get("total_price")),
                confidence=item_data.get("confidence"),
            )
        )

    confidence_scores = {}
    for field_name, score_data in parsed.get("confidence_scores", {}).items():
        confidence_scores[field_name] = ConfidenceScore(
            value=score_data["value"],
            label=score_data["label"],
        )

    return InvoiceExtractionResult(
        vendor=vendor_info,
        invoice_number=parsed.get("invoice_number"),
        invoice_date=parse_date(parsed.get("invoice_date")),
        due_date=parse_date(parsed.get("due_date")),
        subtotal=normalize_amount(parsed.get("subtotal")),
        tax_amount=normalize_amount(parsed.get("tax_amount")),
        total_amount=normalize_amount(parsed.get("total_amount")),
        currency=parsed.get("currency"),
        line_items=line_items,
        raw_fields=parsed.get("raw_fields", {}),
        confidence_scores=confidence_scores,
        document_type="invoice",
    )
