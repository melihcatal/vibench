import io
from typing import Optional, List
from document_client import get_document_intelligence_client
from document_models import ExtractedReceipt, ExtractedField, ReceiptItem
from azure.ai.formrecognizer import AnalyzeResult


def extract_receipt_fields(receipt_data: bytes) -> ExtractedReceipt:
    document_analysis_client = get_document_intelligence_client()

    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-receipt", receipt_data
    )
    receipts: AnalyzeResult = poller.result()

    if not receipts.documents:
        return ExtractedReceipt()

    receipt = receipts.documents[0]

    merchant_name = (
        ExtractedField(
            receipt.fields.get("MerchantName").content,
            receipt.fields.get("MerchantName").confidence,
        )
        if receipt.fields.get("MerchantName")
        else None
    )
    transaction_date = (
        ExtractedField(
            str(receipt.fields.get("TransactionDate").value),
            receipt.fields.get("TransactionDate").confidence,
        )
        if receipt.fields.get("TransactionDate")
        else None
    )
    total_amount = (
        ExtractedField(
            receipt.fields.get("Total").value, receipt.fields.get("Total").confidence
        )
        if receipt.fields.get("Total")
        else None
    )
    total_tax = (
        ExtractedField(
            receipt.fields.get("TotalTax").value,
            receipt.fields.get("TotalTax").confidence,
        )
        if receipt.fields.get("TotalTax")
        else None
    )
    currency = (
        ExtractedField(
            receipt.fields.get("Currency").value,
            receipt.fields.get("Currency").confidence,
        )
        if receipt.fields.get("Currency")
        else None
    )
    merchant_address = (
        ExtractedField(
            receipt.fields.get("MerchantAddress").content,
            receipt.fields.get("MerchantAddress").confidence,
        )
        if receipt.fields.get("MerchantAddress")
        else None
    )

    items: List[ReceiptItem] = []
    if receipt.fields.get("Items") and receipt.fields.get("Items").value:
        for item in receipt.fields.get("Items").value:
            item_description = (
                item.value.get("Description").value
                if item.value.get("Description")
                else None
            )
            item_quantity = (
                item.value.get("Quantity").value if item.value.get("Quantity") else None
            )
            item_price = (
                item.value.get("Price").value if item.value.get("Price") else None
            )
            item_total_price = (
                item.value.get("Total").value if item.value.get("Total") else None
            )
            items.append(
                ReceiptItem(
                    description=item_description,
                    quantity=item_quantity,
                    price=item_price,
                    total_price=item_total_price,
                )
            )

    return ExtractedReceipt(
        merchant_name=merchant_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        total_tax=total_tax,
        items=items,
        currency=currency,
        merchant_address=merchant_address,
    )
