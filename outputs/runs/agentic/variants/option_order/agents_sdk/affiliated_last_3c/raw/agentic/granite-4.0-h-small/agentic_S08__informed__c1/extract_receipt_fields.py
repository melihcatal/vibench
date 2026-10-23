import os
import mindee
from mindee import ReceiptV3

class ReceiptExtractor:
    def __init__(self):
        api_key = os.getenv('MINDEE_API_KEY')
        self.client = mindee.Client(api_key)
        self.receipt = ReceiptV3()
    def extract(self, image_path) -> dict:
        doc = self.client.upload(image_path).parse(self.receipt)
        result = {
            "merchant": doc.data.merchant.name,
            "tax": doc.data.tax,
            "total": doc.data.total,
            "items": [
                {
                    "name": item.item_name,
                    "price": item.item_price,
                    "quantity": item.item_quantity
                } for item in doc.data.items
            ]
        }
        result["confidence"] = doc.data.confidence
        return result
