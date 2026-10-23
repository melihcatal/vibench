import os
from mindee import MindeeClient, ReceiptV4


class ExtractReceiptFields:
    def __init__(self):
        # Mindee requires API key in environment variable
        self.client = MindeeClient(api_key=os.getenv("MINDEE_API_KEY"))

    def process(self, file_path):
        # Load receipt document
        with open(file_path, "rb") as f:
            doc = self.client.process_receipt(file_path)
            receipt = doc.json()
            # Extract required fields
            merchant = receipt.get("merchant", {}).get("name")
            tax = receipt.get("tax")
            total = receipt.get("total")
            items = [
                {
                    "name": item.get("name"),
                    "qty": item.get("quantity"),
                    "price": item.get("price"),
                    "total": item.get("amount"),
                }
                for item in receipt.get("items", [])
            ]
            return {"merchant": merchant, "tax": tax, "total": total, "items": items}
