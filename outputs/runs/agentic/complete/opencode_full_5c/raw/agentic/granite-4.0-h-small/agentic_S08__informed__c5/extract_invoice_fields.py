import os
from document_client import DocumentClient

# Azure Document Intelligence prebuilt invoice
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")


class ExtractInvoiceFields:
    def __init__(self):
        self.client = DocumentClient(
            endpoint=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
            key=AZURE_DOCUMENT_INTELLIGENCE_KEY,
        )

    def extract(self, invoice_file_path):
        # Call Azure Document Intelligence prebuilt invoice API
        response = self.client.analyze_invoice(invoice_file_path)
        # response includes vendor, date, total, line_items
        return {
            "vendor": response["vendor"],
            "date": response["date"],
            "total": response["total"],
            "line_items": response["line_items"],
        }
