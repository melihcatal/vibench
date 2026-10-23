import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

from document_client import get_azure_document_intelligence_client
from document_models import ExtractedReceipt, ReceiptItem

def extract_receipt_from_url(
    receipt_url: str,
) -> ExtractedReceipt:
    """
    Extracts structured data from a receipt using Azure Document Intelligence.
    """
    client = get_azure_document_intelligence_client()

    # The model "prebuilt-receipt" is a pre-trained model provided by Azure.
    poller = client.begin_analyze_document_from_url(
        "prebuilt-receipt", receipt_url
    )
    receipts = poller.result()

    if not receipts.documents:
        raise ValueError("Failed to extract any receipts from the document.")

    # Assuming the first document is the receipt of interest
    extracted = receipts.documents[0]
    
    def get_field_value(field_name):
        field = extracted.fields.get(field_name)
        return field.value if field else None
    
    items = []
    item_list = extracted.fields.get("Items")
    if item_list and item_list.value:
        for item_data in item_list.value:
            item_fields = item_data.value
            item = ReceiptItem(
                description=item_fields.get("Description").value if item_fields.get("Description") else "N/A",
                quantity=item_fields.get("Quantity").value if item_fields.get("Quantity") else None,
                total_price=item_fields.get("TotalPrice").value if item_fields.get("TotalPrice") else None,
            )
            items.append(item)

    receipt = ExtractedReceipt(
        merchant_name=get_field_value("MerchantName"),
        transaction_date=str(get_field_value("TransactionDate")),
        transaction_time=str(get_field_value("TransactionTime")),
        total=get_field_value("Total"),
        tax=get_field_value("TotalTax"),
        items=items,
        raw_fields={k: v.content for k, v in extracted.fields.items() if v},
    )

    return receipt
