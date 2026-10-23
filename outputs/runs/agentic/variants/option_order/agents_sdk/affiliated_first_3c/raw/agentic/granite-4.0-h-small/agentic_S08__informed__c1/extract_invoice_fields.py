import os
import mindee

# Mindee SDK import (concrete provider)
from mindee import MindeeClient

class InvoiceExtractor:
    def __init__(self, api_key: str = None):
        self.client = MindeeClient(api_key or os.getenv('MINDEE_API_KEY'))

    def extract(self, file_path: str):
        doc = self.client.process_invoice(file_path)
        # Assume mindee returns a dict with fields: vendor, date, total, line_items
        result = {
            "vendor": doc.get('vendor'),
            "date": doc.get('date'),
            "total": doc.get('total'),
            "line_items": doc.get('line_items')
        }
        return result
