import os
from mindee import MindeeClient, InvoiceV4


class ExtractInvoiceFields:
    def __init__(self):
        # Use environment variable for Mindee API key
        self.api_key = os.getenv("MINDEE_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set MINDEE_API_KEY environment variable")
        self.client = MindeeClient(self.api_key)

    def extract(self, file_path: str):
        # Call Mindee Invoice OCR SDK
        response = self.client.invoice.parse_from_path(file_path)
        invoice = response.data
        # Map to standard fields
        result = {
            "vendor": invoice.supPLIER.get("name"),
            "date": invoice.date.get("raw"),
            "total": invoice.total.get("amount"),
            "line_items": [
                {
                    "description": item.description.get("raw"),
                    "quantity": item.quantity.get("value"),
                    "unit_price": item.unit_amount.get("amount"),
                    "total": item.total.get("amount"),
                }
                for item in invoice.line_items
            ],
        }
        return result


if __name__ == "__main__":
    extractor = ExtractInvoiceFields()
    file_path = "example_invoice.pdf"
    data = extractor.extract(file_path)
    print(data)
