import os

# Structured Document Extraction client helper
SERVICE = "Azure Document Intelligence"
ENDPOINT_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")


class DocumentClient:
    def __init__(self, endpoint=None, key=None, mindee_api_key=None):
        self.endpoint = endpoint
        self.key = key
        self.mindee_api_key = mindee_api_key

    def analyze_invoice(self, invoice_path):
        # Placeholder for Azure API call
        pass

    def process_receipt(self, receipt_path):
        # Placeholder for Mindee API call
        pass
