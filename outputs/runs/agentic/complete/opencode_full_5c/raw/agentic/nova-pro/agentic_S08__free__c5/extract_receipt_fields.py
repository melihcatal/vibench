import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def extract_fields(document_path):
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
    with open(document_path, "rb") as document_file:
        poller = client.begin_analyze_document("prebuilt-document", document_file)
        result = poller.result()
        merchant = result.documents[0].fields.get("Merchant", {}).get("value", "")
        tax = result.documents[0].fields.get("Tax", {}).get("value", "")
        total = result.documents[0].fields.get("Total", {}).get("value", "")
        items = result.documents[0].fields.get("Items", {}).get("value", [])
        return {"merchant": merchant, "tax": tax, "total": total, "items": items}
