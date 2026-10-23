import os
from azure.ai.documentintelligence.models import AnalyzeResult
from document_client import get_azure_document_intelligence_client
from document_models import ExtractedReceipt, ReceiptItem


def extract_receipt_fields(file_content: bytes) -> ExtractedReceipt:
    client = get_azure_document_intelligence_client()

    poller = client.begin_analyze_document(
        model_id="prebuilt-receipt",
        analyze_request=file_content,
        content_type="application/octet-stream",
    )
    result: AnalyzeResult = poller.result()

    merchant_name = None
    tax_amount = None
    total_amount = None
    items = []

    if result.documents:
        receipt = result.documents[0]
        if receipt.fields:
            if "MerchantName" in receipt.fields:
                merchant_name = receipt.fields["MerchantName"].content
            if "TotalTax" in receipt.fields:
                tax_amount = receipt.fields["TotalTax"].value_number
            if "Total" in receipt.fields:
                total_amount = receipt.fields["Total"].value_number

            if "Items" in receipt.fields and receipt.fields["Items"].value_array:
                for item_field in receipt.fields["Items"].value_array:
                    if item_field.value_object:
                        item_description = None
                        item_quantity = None
                        item_price = None
                        if "Description" in item_field.value_object:
                            item_description = item_field.value_object[
                                "Description"
                            ].content
                        if "Quantity" in item_field.value_object:
                            item_quantity = item_field.value_object[
                                "Quantity"
                            ].value_number
                        if "TotalPrice" in item_field.value_object:
                            item_price = item_field.value_object[
                                "TotalPrice"
                            ].value_number

                        if item_description:
                            items.append(
                                ReceiptItem(
                                    description=item_description,
                                    quantity=item_quantity,
                                    price=item_price,
                                )
                            )

    return ExtractedReceipt(
        merchant_name=merchant_name,
        tax_amount=tax_amount,
        total_amount=total_amount,
        items=items,
    )
