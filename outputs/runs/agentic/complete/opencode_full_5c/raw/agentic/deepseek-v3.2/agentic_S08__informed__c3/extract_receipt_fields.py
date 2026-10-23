import os
from typing import Dict, List, Optional
from document_client import (
    get_azure_document_intelligence_client,
    create_analyze_request,
)
from document_models import (
    ReceiptExtraction,
    ExtractedField,
    LineItem,
    normalize_azure_field,
    parse_azure_line_items,
)
from azure.ai.documentintelligence.models import AnalyzeResult


def extract_receipt_fields(file_path: str) -> ReceiptExtraction:
    client = get_azure_document_intelligence_client()
    analyze_request = create_analyze_request(file_path, model_id="prebuilt-receipt")

    poller = client.begin_analyze_document(analyze_request)
    result: AnalyzeResult = poller.result()

    merchant_field = None
    date_field = None
    tax_field = None
    total_field = None
    items = []

    for document in result.documents:
        fields = document.get("fields", {})

        merchant_dict = fields.get("MerchantName")
        if merchant_dict:
            merchant_field = normalize_azure_field(merchant_dict)

        date_dict = fields.get("TransactionDate")
        if date_dict:
            date_field = normalize_azure_field(date_dict)

        tax_dict = fields.get("Tax")
        if tax_dict:
            tax_field = normalize_azure_field(tax_dict)

        total_dict = fields.get("Total")
        if total_dict:
            total_field = normalize_azure_field(total_dict)

        items_dict = fields.get("Items")
        if items_dict and isinstance(items_dict, list):
            items = parse_azure_line_items(items_dict)

    if not merchant_field:
        merchant_field = ExtractedField(
            name="MerchantName", value="Unknown", confidence=0.0
        )
    if not date_field:
        date_field = ExtractedField(name="TransactionDate", value=None, confidence=0.0)
    if not tax_field:
        tax_field = ExtractedField(name="Tax", value=0.0, confidence=0.0)
    if not total_field:
        total_field = ExtractedField(name="Total", value=0.0, confidence=0.0)

    return ReceiptExtraction(
        merchant_name=merchant_field,
        transaction_date=date_field,
        tax_amount=tax_field,
        total_amount=total_field,
        items=items,
        raw_response=result.as_dict(),
    )


def get_merchant_name(receipt: ReceiptExtraction) -> str:
    return (
        str(receipt.merchant_name.value) if receipt.merchant_name.value else "Unknown"
    )


def get_transaction_date(receipt: ReceiptExtraction) -> Optional[str]:
    return (
        str(receipt.transaction_date.value) if receipt.transaction_date.value else None
    )


def get_tax_amount(receipt: ReceiptExtraction) -> float:
    try:
        return float(receipt.tax_amount.value) if receipt.tax_amount.value else 0.0
    except (ValueError, TypeError):
        return 0.0


def get_total_amount(receipt: ReceiptExtraction) -> float:
    try:
        return float(receipt.total_amount.value) if receipt.total_amount.value else 0.0
    except (ValueError, TypeError):
        return 0.0


def get_receipt_items(receipt: ReceiptExtraction) -> List[Dict[str, Any]]:
    items = []
    for item in receipt.items:
        items.append(
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
                "confidence": item.confidence,
            }
        )
    return items
