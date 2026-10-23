"""
Extract receipt fields using Mindee Invoice & Receipt OCR API.

Provider: Mindee (Receipt OCR)
SDK: mindee
Auth: MINDEE_API_KEY
Model: mindee/receipt_v5
"""

import os
from typing import Optional

from mindee import Client, PredictResponse
from mindee.parsing.standard import AmountField, DateField, StringField

from document_models import (
    ReceiptExtractionResult,
    LineItem,
)
from document_client import (
    load_env_var,
    normalize_amount,
    normalize_date,
)


def _get_mindee_client() -> Client:
    """Create and return an authenticated Mindee client."""
    api_key = load_env_var("MINDEE_API_KEY")
    if not api_key:
        raise EnvironmentError("MINDEE_API_KEY environment variable is not set")
    return Client(api_key=api_key)


def extract_receipt_fields_from_file(
    file_path: str,
) -> ReceiptExtractionResult:
    """
    Extract merchant, tax, total, and items from a receipt
    using Mindee Receipt OCR (mindee/receipt_v5).

    Args:
        file_path: Path to the receipt file (image or PDF).

    Returns:
        ReceiptExtractionResult with standardized extracted fields.
    """
    client = _get_mindee_client()

    with open(file_path, "rb") as f:
        response: PredictResponse = client.parse(
            "mindee/receipt_v5",
            input_source=f,
        )

    return _parse_mindee_receipt_response(response)


def extract_receipt_fields_from_bytes(
    file_bytes: bytes,
    filename: str = "receipt.jpg",
) -> ReceiptExtractionResult:
    """
    Extract receipt fields from raw bytes using Mindee Receipt OCR.

    Args:
        file_bytes: Raw bytes of the receipt file.
        filename: Original filename for content-type detection.

    Returns:
        ReceiptExtractionResult with extracted fields.
    """
    from io import BytesIO

    client = _get_mindee_client()
    file_io = BytesIO(file_bytes)
    file_io.name = filename

    response: PredictResponse = client.parse(
        "mindee/receipt_v5",
        input_source=file_io,
    )

    return _parse_mindee_receipt_response(response)


def extract_receipt_fields_from_url(
    file_url: str,
) -> ReceiptExtractionResult:
    """
    Extract receipt fields from a URL using Mindee Receipt OCR.

    Args:
        file_url: URL pointing to the receipt file.

    Returns:
        ReceiptExtractionResult with extracted fields.
    """
    client = _get_mindee_client()

    from mindee.input import InputSource

    input_source = InputSource.from_url(file_url)
    response: PredictResponse = client.parse(
        "mindee/receipt_v5",
        input_source=input_source,
    )

    return _parse_mindee_receipt_response(response)


def _parse_mindee_receipt_response(
    response: PredictResponse,
) -> ReceiptExtractionResult:
    """
    Parse a Mindee PredictResponse into a standardized ReceiptExtractionResult.
    """
    result = ReceiptExtractionResult(
        provider="mindee",
        model_id="mindee/receipt_v5",
    )

    prediction = response.document.prediction

    # Merchant name
    merchant = prediction.supplier
    if merchant and merchant.name:
        result.merchant_name = str(merchant.name)
        result.merchant_confidence = float(merchant.confidence) if hasattr(merchant, "confidence") and merchant.confidence else 0.0
    elif hasattr(prediction, "supplier_name") and prediction.supplier_name:
        result.merchant_name = str(prediction.supplier_name)
        result.merchant_confidence = 1.0

    # Receipt date
    if prediction.date:
        date_field = prediction.date
        if isinstance(date_field, DateField) and date_field.value:
            result.receipt_date = date_field.value.strftime("%Y-%m-%d")
        elif hasattr(date_field, "value") and date_field.value:
            result.receipt_date = normalize_date(str(date_field.value))
        result.receipt_date_confidence = (
            float(date_field.confidence)
            if hasattr(date_field, "confidence") and date_field.confidence
            else 0.0
        )

    # Total amount
    if prediction.total_amount:
        total_field = prediction.total_amount
        if isinstance(total_field, AmountField) and total_field.value is not None:
            result.total_amount = float(total_field.value)
        elif hasattr(total_field, "value") and total_field.value is not None:
            result.total_amount = float(total_field.value)
        result.total_confidence = (
            float(total_field.confidence)
            if hasattr(total_field, "confidence") and total_field.confidence
            else 0.0
        )

    # Tax amount
    if prediction.taxes and len(prediction.taxes) > 0:
        total_tax = sum(float(t.value) for t in prediction.taxes if t.value is not None)
        result.tax_amount = total_tax
        tax_confidences = [t.confidence for t in prediction.taxes if t.confidence]
        if tax_confidences:
            result.tax_confidence = float(sum(tax_confidences) / len(tax_confidences))
        else:
            result.tax_confidence = 0.0

    # Line items
    if hasattr(prediction, "line_items") and prediction.line_items:
        for li in prediction.line_items:
            line_item = LineItem(
                description=str(getattr(li, "description", getattr(li, "name", ""))),
                quantity=float(getattr(li, "quantity", 0) or 0) if getattr(li, "quantity", None) is not None else None,
                unit_price=float(getattr(li, "unit_price", 0) or 0) if getattr(li, "unit_price", None) is not None else None,
                total_price=float(getattr(li, "total_amount", 0) or 0) if getattr(li, "total_amount", None) is not None else None,
                confidence=float(getattr(li, "confidence", 1.0)) if getattr(li, "confidence", None) is not None else 1.0,
            )
            result.items.append(line_item)

    # Build raw response for debugging/storage
    result.raw_response = _build_raw_response(prediction)

    return result


def _build_raw_response(prediction) -> dict:
    """Build a raw response dict from Mindee prediction object."""
    raw = {}
    if hasattr(prediction, "supplier"):
        raw["supplier"] = {
            "name": str(prediction.supplier.name) if prediction.supplier and prediction.supplier.name else None,
        }
    if hasattr(prediction, "date") and prediction.date:
        raw["date"] = str(prediction.date.value) if hasattr(prediction.date, "value") else str(prediction.date)
    if hasattr(prediction, "total_amount") and prediction.total_amount:
        raw["total_amount"] = float(prediction.total_amount.value) if hasattr(prediction.total_amount, "value") else float(prediction.total_amount)
    if hasattr(prediction, "taxes") and prediction.taxes:
        raw["taxes"] = [
            {"rate": str(t.rate), "value": str(t.value)}
            for t in prediction.taxes
        ]
    return raw
