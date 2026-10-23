import os
from document_client import DocumentClient

# Mindee invoice OCR
MINDEE_API_KEY = os.getenv("MINDEE_API_KEY")


class ExtractReceiptFields:
    def __init__(self):
        self.client = DocumentClient(mindee_api_key=MINDEE_API_KEY)

    def extract(self, receipt_image_path):
        # Call Mindee invoice OCR API
        response = self.client.process_receipt(receipt_image_path)
        # response includes merchant, tax, total, items
        return {
            "merchant": response["merchant"],
            "tax": response["tax"],
            "total": response["total"],
            "items": response["items"],
        }
