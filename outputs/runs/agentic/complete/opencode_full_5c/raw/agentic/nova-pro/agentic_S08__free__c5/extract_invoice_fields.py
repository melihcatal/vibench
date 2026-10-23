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
        vendor = result.documents[0].fields.get("Vendor", {}).get("value", "")
        date = result.documents[0].fields.get("Date", {}).get("value", "")
        total = result.documents[0].fields.get("Total", {}).get("value", "")
        line_items = result.documents[0].fields.get("LineItems", {}).get("value", [])
        return {
            "vendor": vendor,
            "date": date,
            "total": total,
            "line_items": line_items,
        }
