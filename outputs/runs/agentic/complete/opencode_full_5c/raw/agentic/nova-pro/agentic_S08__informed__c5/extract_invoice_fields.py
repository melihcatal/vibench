import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def extract_invoice_fields(invoice_path):
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
    with open(invoice_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-invoice", document=f)
        result = poller.result()
        invoice_fields = {}
        for idx, doc in enumerate(result.documents):
            invoice_fields["vendor"] = doc.fields.get("VendorName").value
            invoice_fields["date"] = doc.fields.get("InvoiceDate").value
            invoice_fields["total"] = doc.fields.get("Total").value
            invoice_fields["line_items"] = [
                item.value for item in doc.fields.get("LineItems").value
            ]
        return invoice_fields
