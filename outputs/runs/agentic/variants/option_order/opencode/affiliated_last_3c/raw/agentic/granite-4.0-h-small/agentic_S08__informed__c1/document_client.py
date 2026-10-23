import os
from mindee import MindeeClient, InvoiceV4, ReceiptV4


class DocumentClient:
    """Local helper providing unified client access for Structured Document Extraction."""

    def __init__(self):
        # Retrieve credentials from environment variables
        self.mindee_api_key = os.getenv("MINDEE_API_KEY")
        if not self.mindee_api_key:
            raise RuntimeError("MINDEE_API_KEY environment variable not set")
        self.client = MindeeClient(self.mindee_api_key)

    def parse_invoice(self, file_path: str) -> dict:
        response = self.client.invoice.parse_from_path(file_path)
        invoice = response.data
        return {
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

    def parse_receipt(self, file_path: str) -> dict:
        response = self.client.receipt.parse_from_path(file_path)
        receipt = response.data
        return {
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


if __name__ == "__main__":
    dc = DocumentClient()
    invoice_data = dc.parse_invoice("example_invoice.pdf")
    receipt_data = dc.parse_receipt("example_receipt.jpg")
    print("Invoice:", invoice_data)
    print("Receipt:", receipt_data)
