import os
from typing import List
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.core.credentials import AzureKeyCredential
from document_models import ReceiptExtractionResult, LineItem
from document_client import get_azure_document_intelligence_client


def extract_receipt_fields(file_content: bytes) -> ReceiptExtractionResult:
    client = get_azure_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-receipt", file_content, content_type="application/octet-stream"
    )
    result: AnalyzeResult = poller.result()

    merchant_name = None
    transaction_date = None
    total_amount = None
    tax_amount = None
    currency = None
    line_items: List[LineItem] = []

    if result.documents:
        receipt = result.documents[0]
        if receipt.fields:
            if (
                "MerchantName" in receipt.fields
                and receipt.fields["MerchantName"].value
            ):
                merchant_name = receipt.fields["MerchantName"].value.content
            if (
                "TransactionDate" in receipt.fields
                and receipt.fields["TransactionDate"].value
            ):
                transaction_date = (
                    receipt.fields["TransactionDate"].value.strftime("%Y-%m-%d")
                    if receipt.fields["TransactionDate"].value
                    else None
                )
            if (
                "Total" in receipt.fields
                and receipt.fields["Total"].value
                and receipt.fields["Total"].value.amount
            ):
                total_amount = receipt.fields["Total"].value.amount
                currency = receipt.fields["Total"].value.currency_symbol
            if (
                "TotalTax" in receipt.fields
                and receipt.fields["TotalTax"].value
                and receipt.fields["TotalTax"].value.amount
            ):
                tax_amount = receipt.fields["TotalTax"].value.amount

            if "Items" in receipt.fields and receipt.fields["Items"].value:
                for item in receipt.fields["Items"].value:
                    description = None
                    quantity = None
                    total_price = None
                    if item.value and item.value.fields:
                        if (
                            "Description" in item.value.fields
                            and item.value.fields["Description"].value
                        ):
                            description = item.value.fields["Description"].value.content
                        if (
                            "Quantity" in item.value.fields
                            and item.value.fields["Quantity"].value
                        ):
                            quantity = item.value.fields["Quantity"].value.as_float()
                        if (
                            "TotalPrice" in item.value.fields
                            and item.value.fields["TotalPrice"].value
                        ):
                            total_price = item.value.fields["TotalPrice"].value.amount
                    if description or quantity or total_price:
                        line_items.append(
                            LineItem(
                                description=description if description else "",
                                quantity=quantity,
                                amount=total_price,
                            )
                        )

    return ReceiptExtractionResult(
        merchant_name=merchant_name,
        transaction_date=transaction_date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        currency=currency,
        line_items=line_items,
        raw_response=result.to_dict(),
    )
