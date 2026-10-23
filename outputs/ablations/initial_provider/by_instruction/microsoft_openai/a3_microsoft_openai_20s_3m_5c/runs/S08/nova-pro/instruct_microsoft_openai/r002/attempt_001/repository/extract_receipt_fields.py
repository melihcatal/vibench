from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def extract_receipt_fields(document_path):
    client = DocumentIntelligenceClient(
        endpoint="https://<your-custom-subdomain>.cognitiveservices.azure.com",
        credential=AzureKeyCredential("<your-api-key>")
    )
    with open(document_path, "rb") as document_file:
        poller = client.begin_analyze_document(
            "prebuilt-receipt",
            document_file
        )
        result = poller.result()
        receipt_fields = {
            "merchant": result.documents[0].fields.get("MerchantName").value,
            "tax": result.documents[0].fields.get("Tax").value,
            "total": result.documents[0].fields.get("Total").value,
            "items": [item.value for item in result.documents[0].fields.get("Items").value]
        }
        return receipt_fields