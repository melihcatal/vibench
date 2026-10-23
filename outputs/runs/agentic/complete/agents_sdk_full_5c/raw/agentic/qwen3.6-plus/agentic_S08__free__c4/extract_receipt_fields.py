"""
[SAME-SCENARIO] Extract merchant, tax, total, and items from a receipt.
Uses AWS Textract (boto3) with the AnalyzeExpense API to extract structured
receipt data from image or PDF files.

Provider: AWS Textract
SDK: boto3
API: textract.analyze_expense
"""

import os
import logging
from typing import Optional, List, Dict, Any

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from document_models import ReceiptExtractionResult, ReceiptItem, ConfidenceScore
from document_client import get_aws_textract_config, validate_provider_config, load_document_bytes

logger = logging.getLogger(__name__)

# AWS Textract AnalyzeExpense API endpoint hostname
AWS_TEXTRACT_ENDPOINT_HOST = "textract.amazonaws.com"


def extract_receipt_fields(
    document_bytes: bytes,
    region_name: Optional[str] = None,
) -> ReceiptExtractionResult:
    """
    Extract merchant, tax, total, and items from a receipt document
    using AWS Textract AnalyzeExpense API.

    Args:
        document_bytes: Raw bytes of the receipt document (image or PDF).
        region_name: AWS region for Textract (defaults to config).

    Returns:
        ReceiptExtractionResult with extracted fields and confidence scores.
    """
    config = get_aws_textract_config()
    if region_name:
        config["region_name"] = region_name

    if not validate_provider_config("aws_textract", config):
        raise ValueError("AWS Textract configuration is incomplete. "
                        "Set AWS_REGION environment variable and ensure AWS credentials are configured.")

    try:
        # Initialize AWS Textract client via boto3
        textract_client = boto3.client(
            "textract",
            region_name=config["region_name"],
        )
    except NoCredentialsError:
        raise ValueError("AWS credentials not found. Configure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")

    logger.info(f"Analyzing receipt with AWS Textract (endpoint: {AWS_TEXTRACT_ENDPOINT_HOST})")

    try:
        # Call AWS Textract AnalyzeExpense API
        response = textract_client.analyze_expense(
            Document={"Bytes": document_bytes},
        )
    except ClientError as e:
        logger.error(f"AWS Textract error: {e.response['Error']['Message']}")
        raise

    # Parse response from AWS Textract AnalyzeExpense
    expense_docs = response.get("ExpenseDocuments", [])
    if not expense_docs:
        raise ValueError("No expense documents found in Textract response")

    # Use the first expense document
    expense_doc = expense_docs[0]
    line_items_groups = expense_doc.get("LineItemGroups", [])
    summary_fields = expense_doc.get("SummaryFields", [])

    # Extract receipt fields from Textract summary
    merchant = _extract_field_by_type(summary_fields, "VENDOR")
    tax_amount = _extract_field_amount_by_type(summary_fields, "TAX")
    total_amount = _extract_field_amount_by_type(summary_fields, "TOTAL")
    transaction_date = _extract_field_by_type(summary_fields, "INVOICE_RECEIPT_DATE")

    # Extract line items
    items = []
    for group in line_items_groups:
        line_items = group.get("LineItems", [])
        for item in line_items:
            line_item_expense_fields = item.get("LineItemExpenseFields", [])
            item_name = _extract_field_by_type(line_item_expense_fields, "ITEM")
            item_price = _extract_field_amount_by_type(line_item_expense_fields, "PRICE")
            item_quantity = _extract_field_amount_by_type(line_item_expense_fields, "QUANTITY")

            items.append(ReceiptItem(
                name=item_name or "",
                price=item_price or 0.0,
                quantity=item_quantity or 1.0,
            ))

    # Build confidence scores from AWS Textract response
    confidence_scores = _build_confidence_from_summary(summary_fields)

    return ReceiptExtractionResult(
        merchant=merchant or "",
        transaction_date=transaction_date or "",
        tax_amount=tax_amount or 0.0,
        total_amount=total_amount or 0.0,
        currency="USD",
        items=items,
        confidence_scores=confidence_scores,
        raw_response={"expense_document_id": expense_doc.get("ExpenseIndex"), "page_count": len(response.get("DocumentMetadata", {}))},
    )


def _extract_field_by_type(summary_fields: List[Dict], field_type: str) -> Optional[str]:
    """Extract a field value by type from AWS Textract summary fields."""
    for field in summary_fields:
        type_detection = field.get("Type", {})
        if type_detection.get("Text") == field_type:
            value_detection = field.get("ValueDetection", {})
            return value_detection.get("Text")
    return None


def _extract_field_amount_by_type(summary_fields: List[Dict], field_type: str) -> Optional[float]:
    """Extract a field numeric amount by type from AWS Textract summary fields."""
    for field in summary_fields:
        type_detection = field.get("Type", {})
        if type_detection.get("Text") == field_type:
            value_detection = field.get("ValueDetection", {})
            text_value = value_detection.get("Text", "")
            # Remove currency symbols and parse
            cleaned = text_value.replace("$", "").replace(",", "").strip()
            try:
                return float(cleaned)
            except (ValueError, TypeError):
                return None
    return None


def _build_confidence_from_summary(summary_fields: List[Dict]) -> List[ConfidenceScore]:
    """Build confidence score list from AWS Textract summary fields."""
    scores = []
    for field in summary_fields:
        type_detection = field.get("Type", {})
        value_detection = field.get("ValueDetection", {})
        field_type = type_detection.get("Text", "")
        confidence = value_detection.get("Confidence", 0.0)
        if field_type:
            scores.append(ConfidenceScore(
                field_name=field_type,
                score=confidence / 100.0,  # Textract returns 0-100 scale
            ))
    return scores


def extract_receipt_from_file(file_path: str) -> ReceiptExtractionResult:
    """
    Extract receipt fields from a local file.

    Args:
        file_path: Path to the receipt file.

    Returns:
        ReceiptExtractionResult with extracted fields.
    """
    document_bytes = load_document_bytes(file_path)
    return extract_receipt_fields(document_bytes)
