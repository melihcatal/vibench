import os
from mindee import MindeeClient, ReceiptV4


class ExtractReceiptFields:
    def __init__(self):
        # Use environment variable for Mindee API key
        self.api_key = os.getenv("MINDEE_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set MINDEE_API_KEY environment variable")
        self.client = MindeeClient(self.api_key)

    def extract(self, file_path: str):
        # Call Mindee Receipt OCR SDK
        response = self.client.receipt.parse_from_path(file_path)
        receipt = response.data
        # Map to standard fields
        result = {
            "merchant": receipt.supPLIER.get("name"),
            "tax": receipt.tax.get("amount"),
            "total": receipt.total.get("amount"),
            "items": [
                {
                    "description": line.description.get("raw"),
                    "quantity": line.quantity.get("value"),
                    "unit_price": line.unit_amount.get("amount"),
                    "total": line.total.get("amount"),
                }
                for line in receipt.lines
            ],
        }
        return result


if __name__ == "__main__":
    extractor = ExtractReceiptFields()
    file_path = "example_receipt.jpg"
    data = extractor.extract(file_path)
    print(data)
