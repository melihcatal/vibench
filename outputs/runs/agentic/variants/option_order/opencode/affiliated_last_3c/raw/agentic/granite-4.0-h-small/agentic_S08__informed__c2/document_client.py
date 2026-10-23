import os
import json


class DocumentClient:
    def __init__(self):
        # Load local config (e.g., credentials path) from environment or file
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.processor_invoice = os.getenv("DOCUMENTAI_INVOICE_PROCESSOR_ID")
        self.processor_receipt = os.getenv("DOCUMENTAI_RECEIPT_PROCESSOR_ID")
        # In a real implementation, initialize SDK client here

    def process_invoice(self, pdf_bytes):
        # Placeholder: in real code would call Google Document AI
        raise NotImplementedError

    def process_receipt(self, image_bytes):
        # Placeholder: call Google Document AI for receipt parsing
        raise NotImplementedError
