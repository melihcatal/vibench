from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

def extract_receipt_fields(receipt_path):
    client = DocumentIntelligenceClient(
        endpoint="https://<your-custom-subdomain>.cognitiveservices.azure.com/", credential=AzureKeyCredential("<your-api-key>")
    )
    with open(receipt_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-receipt", document=f)
        result = poller.result()
    merchant = result.documents[0].fields.get("MerchantName").value
    tax = result.documents[0].fields.get("Tax").value
    total = result.documents[0].fields.get("Total").value
    items = [item.value for item in result.documents[0].fields.get("Items").value]
    return merchant, tax, total, items