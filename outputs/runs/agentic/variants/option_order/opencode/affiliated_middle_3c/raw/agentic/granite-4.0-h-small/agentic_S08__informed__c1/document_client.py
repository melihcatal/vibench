import os
import mindee
from mindee import MindeeClient


class DocumentClient:
    """Local helper providing common configuration and client utilities for the same-scenario extractors."""

    def __init__(self):
        # Load credentials from environment variables
        self.api_key = os.getenv("MINDEE_API_KEY")
        if not self.api_key:
            raise RuntimeError("Environment variable MINDEE_API_KEY not set")
        self.client = MindeeClient(self.api_key)

    def load_invoice(self, path: str):
        """Parse and return Mindee Invoice OCR result."""
        with open(path, "rb") as f:
            return self.client.invoices.parse_document(f)

    def load_receipt(self, path: str):
        """Parse and return Mindee Receipt OCR result."""
        with open(path, "rb") as f:
            return self.client.receipts.parse_document(f)

    @staticmethod
    def normalise_response(source: str, raw: dict) -> dict:
        """Convert Mindee response into the normalised expense schema used later."""
        return normalize_expense(raw)
