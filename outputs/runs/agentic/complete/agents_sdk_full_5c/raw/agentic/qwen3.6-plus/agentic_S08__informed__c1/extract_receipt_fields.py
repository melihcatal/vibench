"""
[SAME-SCENARIO] Extract merchant, tax, total, and items from a receipt using Mindee Receipt OCR API.

Uses the Mindee SDK (mindee package) with the v5 Receipt API to extract structured fields
from uploaded receipt documents (PDF or image).
Provider: Mindee - Receipt OCR
SDK: mindee
Auth: MINDEE_API_KEY
"""

from __future__ import annotations

import os
from typing import Dict, Optional

from mindee import Client

from document_client import (
    create_mindee_client,
    load_document_bytes,
    detect_mime_type,
    parse_mindee_receipt_response,
)
from document_models import (
    ReceiptExtractionResult,
    VendorInfo,
    LineItem,
    ConfidenceScore,
    parse_date,
    normalize_amount,
)


def extract_receipt_fields(
    file_path: Optional[str] = None,
    file_bytes: Optional[bytes] = None,
    client: Optional[Client] = None,
) -> ReceiptExtractionResult:
    """
    Extract structured fields from a receipt document using Mindee Receipt OCR.

    Extracts:
    - merchant (name, address, phone)
    - receipt_date / receipt_time
    - total_amount
    - tax_amount
    - items (description, quantity, unit_price, total_price)
    - payment_method

    Args:
        file_path: Path to the receipt document (PDF or image).
        file_bytes: Raw bytes of the receipt document (alternative to file_path).
        client: Optional pre-configured Mindee client.

    Returns:
        ReceiptExtractionResult with all extracted fields and confidence scores.
    """
    if client is None:
        client = create_mindee_client()

    if file_bytes is None:
        if file_path is None:
            raise ValueError("Either file_path or file_bytes must be provided")
        file_bytes = load_document_bytes(file_path)

    # Call Mindee Receipt API v5
    response = client.parse(
        input_doc=file_bytes,
        doc_class="expense_receipts_v5",
    )

    parsed = parse_mindee_receipt_response(response)

    # Build merchant info
    merchant_info = None
    if parsed.get("merchant"):
        m = parsed["merchant"]
        merchant_info = VendorInfo(
            name=m.get("name"),
            address=m.get("address"),
            phone=m.get("phone_number"),
        )

    # Build line items
    items = []
    for item_data in parsed.get("items", []):
        items.append(
            LineItem(
                description=item_data.get("description", ""),
                quantity=item_data.get("quantity"),
                unit_price=normalize_amount(item_data.get("unit_price")),
                total_price=normalize_amount(item_data.get("total_price")),
                confidence=item_data.get("confidence"),
            )
        )

    # Build confidence scores
    confidence_scores = {}
    for field_name, score_data in parsed.get("confidence_scores", {}).items():
        confidence_scores[field_name] = ConfidenceScore(
            value=score_data["value"],
            label=score_data["label"],
        )

    return ReceiptExtractionResult(
        merchant=merchant_info,
        receipt_number=parsed.get("receipt_number"),
        receipt_date=parse_date(parsed.get("receipt_date")),
        receipt_time=parsed.get("receipt_time"),
        tax_amount=normalize_amount(parsed.get("tax_amount")),
        tip_amount=normalize_amount(parsed.get("tip_amount")),
        total_amount=normalize_amount(parsed.get("total_amount")),
        currency=parsed.get("currency"),
        items=items,
        payment_method=parsed.get("payment_method"),
        raw_fields=parsed.get("raw_fields", {}),
        confidence_scores=confidence_scores,
        document_type="receipt",
    )


def extract_receipt_fields_from_url(
    file_url: str,
    client: Optional[Client] = None,
) -> ReceiptExtractionResult:
    """
    Extract structured fields from a receipt at a remote URL using Mindee Receipt OCR.

    Args:
        file_url: URL pointing to the receipt document.
        client: Optional pre-configured Mindee client.

    Returns:
        ReceiptExtractionResult with all extracted fields.
    """
    if client is None:
        client = create_mindee_client()

    response = client.parse(
        input_doc=file_url,
        doc_class="expense_receipts_v5",
    )

    parsed = parse_mindee_receipt_response(response)

    merchant_info = None
    if parsed.get("merchant"):
        m = parsed["merchant"]
        merchant_info = VendorInfo(
            name=m.get("name"),
            address=m.get("address"),
            phone=m.get("phone_number"),
        )

    items = []
    for item_data in parsed.get("items", []):
        items.append(
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

    return ReceiptExtractionResult(
        merchant=merchant_info,
        receipt_number=parsed.get("receipt_number"),
        receipt_date=parse_date(parsed.get("receipt_date")),
        receipt_time=parsed.get("receipt_time"),
        tax_amount=normalize_amount(parsed.get("tax_amount")),
        tip_amount=normalize_amount(parsed.get("tip_amount")),
        total_amount=normalize_amount(parsed.get("total_amount")),
        currency=parsed.get("currency"),
        items=items,
        payment_method=parsed.get("payment_method"),
        raw_fields=parsed.get("raw_fields", {}),
        confidence_scores=confidence_scores,
        document_type="receipt",
    )
