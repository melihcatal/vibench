import os
from mindee import MindeeClient


class DocumentClient:
    def __init__(self):
        # Initialize Mindee client using API key from env
        api_key = os.getenv("MINDEE_API_KEY")
        if not api_key:
            raise RuntimeError("MINDEE_API_KEY environment variable not set")
        self.client = MindeeClient(api_key=api_key)

    def extract(self, file_path, doc_type="invoice"):
        if doc_type == "invoice":
            return self.client.process_invoice(file_path)
        elif doc_type == "receipt":
            return self.client.process_receipt(file_path)
        else:
            raise ValueError("Unsupported document type")
