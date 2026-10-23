from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

# Initialize the client
client = DocumentIntelligenceClient(
    endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")),
)


def extract_receipt_fields(receipt_path):
    with open(receipt_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-receipt", document=f)
        result = poller.result()
        # Extract fields
        merchant = result.merchant_name
        tax = result.tax
        total = result.total
        items = result.items
        return merchant, tax, total, items
