from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os

def extract_receipt_fields(endpoint: str, key: str, receipt_path: str) -> dict:
    """
    Extracts merchant, tax, total, and items from a receipt using Azure Form Recognizer.
    """
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(receipt_path, "rb") as f:
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-receipt", document=f.read()
        )
    receipts = poller.result()

    extracted_fields = {
        "merchant_name": None,
        "tax_amount": None,
        "total_amount": None,
        "items": []
    }

    for idx, receipt in enumerate(receipts.documents):
        if receipt.fields.get("MerchantName"):
            extracted_fields["merchant_name"] = receipt.fields.get("MerchantName").value
        if receipt.fields.get("TotalTax"):
            extracted_fields["tax_amount"] = receipt.fields.get("TotalTax").value
        if receipt.fields.get("Total"):
            extracted_fields["total_amount"] = receipt.fields.get("Total").value
        
        if receipt.fields.get("Items"):
            for item in receipt.fields.get("Items").value:
                item_data = {}
                if item.value.get("Description"):
                    item_data["description"] = item.value.get("Description").value
                if item.value.get("TotalPrice"):
                    item_data["total_price"] = item.value.get("TotalPrice").value
                extracted_fields["items"].append(item_data)
    
    return extracted_fields
