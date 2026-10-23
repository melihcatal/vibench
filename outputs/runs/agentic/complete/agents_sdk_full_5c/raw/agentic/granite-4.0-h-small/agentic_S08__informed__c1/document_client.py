import os
from mindee import MindeeClient


class MindeeClient:
    def __init__(self, api_key: str | None = None):
        # Use env var MINDEE_API_KEY or explicit key
        api_key = api_key or os.getenv("MINDEE_API_KEY")
        if not api_key:
            raise RuntimeError("MINDEE_API_KEY must be set")
        self.client = MindeeClient(api_key=api_key)

    def process_invoice(self, file_bytes: bytes) -> Any:
        # Example usage of Mindee Invoice OCR SDK
        invoice_doc = self.client.parse_invoice(file_bytes)
        return invoice_doc


class GenericClient:
    # Placeholder for other providers
    pass
