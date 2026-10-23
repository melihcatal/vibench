import os
from mindee import MindeeClient, InvoiceV4


class ExtractInvoiceFields:
    def __init__(self):
        # Mindee requires API key in environment variable
        self.client = MindeeClient(api_key=os.getenv("MINDEE_API_KEY"))

    def process(self, file_path):
        # Load invoice document
        with open(file_path, "rb") as f:
            doc = self.client.process_invoice(file_path)
            invoice = doc.json()
            # Extract required fields
            vendor = invoice.get("vendor", {}).get("name")
            date = invoice.get("date")
            total = invoice.get("total")
            line_items = [
                {
                    "description": item.get("description"),
                    "quantity": item.get("quantity"),
                    "unit_price": item.get("unit_price"),
                    "amount": item.get("amount"),
                }
                for item in invoice.get("items", [])
            ]
            return {
                "vendor": vendor,
                "date": date,
                "total": total,
                "line_items": line_items,
            }
