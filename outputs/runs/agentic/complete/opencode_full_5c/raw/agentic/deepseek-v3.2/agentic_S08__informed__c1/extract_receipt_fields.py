import os
from typing import Dict, Any, List
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential


def extract_receipt_fields(receipt_path: str) -> Dict[str, Any]:
    """
    Extract merchant, tax, total, and items from a receipt using Azure Document Intelligence.
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not configured")

    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )

    with open(receipt_path, "rb") as f:
        document_content = f.read()

    poller = client.begin_analyze_document(
        "prebuilt-receipt", AnalyzeDocumentRequest(bytes_source=document_content)
    )
    result = poller.result()

    extracted_fields = {"merchant": None, "tax": None, "total": None, "items": []}

    if result.documents:
        receipt = result.documents[0]
        fields = receipt.fields

        if "MerchantName" in fields:
            extracted_fields["merchant"] = fields["MerchantName"].value_string

        if "TotalTax" in fields:
            extracted_fields["tax"] = float(fields["TotalTax"].value_number)

        if "Total" in fields:
            extracted_fields["total"] = float(fields["Total"].value_number)

        if "Items" in fields:
            items = fields["Items"].value_array
            for item in items:
                item_fields = item.value_object
                receipt_item = {}
                if "Description" in item_fields:
                    receipt_item["description"] = item_fields[
                        "Description"
                    ].value_string
                if "TotalPrice" in item_fields:
                    receipt_item["price"] = float(
                        item_fields["TotalPrice"].value_number
                    )
                if "Quantity" in item_fields:
                    receipt_item["quantity"] = float(
                        item_fields["Quantity"].value_number
                    )
                extracted_fields["items"].append(receipt_item)

    return extracted_fields
