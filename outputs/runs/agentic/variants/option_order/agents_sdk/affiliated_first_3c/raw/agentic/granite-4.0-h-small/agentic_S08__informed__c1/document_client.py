import os
import mindee

class DocumentClient:
    """
    Central client wrapper for structured document extraction.
    Currently supports Mindee invoice OCR as the concrete provider.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('MINDEE_API_KEY')
        if not self.api_key:
            raise ValueError('MINDEE_API_KEY must be set')
        self.client = mindee.MindeeClient(self.api_key)

    def process_invoice(self, file_path: str):
        """Delegates to Mindee invoice OCR endpoint."""
        doc = self.client.process_invoice(file_path)
        # The raw response contains many fields; we expose only the ones we need.
        return {
            'vendor': doc.get('vendor'),
            'date': doc.get('date'),
            'total': doc.get('total'),
            'line_items': doc.get('line_items')
        }
