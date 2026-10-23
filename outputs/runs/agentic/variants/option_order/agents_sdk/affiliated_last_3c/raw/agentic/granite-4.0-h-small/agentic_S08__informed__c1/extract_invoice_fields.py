import os
import mindee
from mindee import InvoiceV3

class InvoiceExtractor:
    def __init__(self):
        api_key = os.getenv('MINDEE_API_KEY')
        self.client = mindee.Client(api_key)
        self.invoice = InvoiceV3()
    def extract(self, image_path) -> dict:
        # Assuming image_path is a local file path
        doc = self.client.upload(image_path).parse(self.invoice)
        result = {
            "vendor": doc.data.vendor.name,
            "date": doc.data.invoice_date,
            "total": doc.data.total,
            "line_items": [
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "amount": item.amount
                } for item in doc.data.items
            ]
        }
        result["confidence"] = doc.data.confidence
        return result
