import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def extract_receipt_fields(receipt_path):
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
    with open(receipt_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-receipt", document=f)
        result = poller.result()
        receipt_fields = {}
        for idx, doc in enumerate(result.documents):
            receipt_fields["merchant"] = doc.fields.get("MerchantName").value
            receipt_fields["tax"] = doc.fields.get("Tax").value
            receipt_fields["total"] = doc.fields.get("Total").value
            receipt_fields["items"] = [
                item.value for item in doc.fields.get("Items").value
            ]
        return receipt_fields
