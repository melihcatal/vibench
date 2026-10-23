from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def extract_invoice_fields(document_path):
    client = DocumentIntelligenceClient(
        endpoint="https://<your-custom-subdomain>.cognitiveservices.azure.com",
        credential=AzureKeyCredential("<your-api-key>")
    )
    with open(document_path, "rb") as document_file:
        poller = client.begin_analyze_document(
            "prebuilt-invoice",
            document_file
        )
        result = poller.result()
        invoice_fields = {
            "vendor": result.documents[0].fields.get("VendorName").value,
            "date": result.documents[0].fields.get("InvoiceDate").value,
            "total": result.documents[0].fields.get("Total").value,
            "line_items": [item.value for item in result.documents[0].fields.get("LineItems").value]
        }
        return invoice_fields