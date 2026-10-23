import os
import mindee

class DocumentClient:
    def __init__(self, api_key: str):
        self.client = mindee.Client(api_key)
        self.invoice = mindee.InvoiceV3()
        self.receipt = mindee.ReceiptV3()
    def parse_invoice(self, image_path: str):
        doc = self.client.upload(image_path).parse(self.invoice)
        return {
            'vendor': doc.data.vendor.name,
            'date': doc.data.invoice_date,
            'total': doc.data.total,
            'line_items': [
                {'description': item.description, 'quantity': item.quantity, 'amount': item.amount}
                for item in doc.data.items
            ],
            'confidence': doc.data.confidence
        }
    def parse_receipt(self, image_path: str):
        doc = self.client.upload(image_path).parse(self.receipt)
        return {
            'merchant': doc.data.merchant.name,
            'tax': doc.data.tax,
            'total': doc.data.total,
            'items': [
                {'name': item.item_name, 'price': item.item_price, 'quantity': item.item_quantity}
                for item in doc.data.items
            ],
            'confidence': doc.data.confidence
        }
