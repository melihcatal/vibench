from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

# Initialize the client
client = DocumentIntelligenceClient(
    endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")),
)


def extract_invoice_fields(invoice_path):
    with open(invoice_path, "rb") as f:
        poller = client.begin_analyze_document("prebuilt-invoice", document=f)
        result = poller.result()
        # Extract fields
        vendor = result.vendor_name
        date = result.invoice_date
        total = result.total
        line_items = result.line_items
        return vendor, date, total, line_items
