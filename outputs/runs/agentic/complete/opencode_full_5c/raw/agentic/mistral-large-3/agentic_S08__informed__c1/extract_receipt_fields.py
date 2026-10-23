from typing import Dict, Any, Optional
import os
from mindee import Client, documents
from mindee.input import LocalInputSource
from mindee.errors import MindeeException


class ReceiptExtractor:
    def __init__(self):
        self.mindee_client = Client(api_key=os.getenv("MINDEE_API_KEY"))

    def extract(self, file_path: str) -> Dict[str, Any]:
        try:
            input_source = LocalInputSource(file_path)
            response = self.mindee_client.parse(
                documents.TypeReceiptV5, input_source=input_source
            )
            return self._normalize_response(response.document)
        except MindeeException as e:
            raise Exception(f"Mindee Receipt extraction failed: {str(e)}")

    def _normalize_response(
        self, document: documents.ReceiptV5Document
    ) -> Dict[str, Any]:
        return {
            "merchant": document.merchant_name.value
            if document.merchant_name
            else None,
            "tax": document.taxes[0].value if document.taxes else None,
            "total": document.total_amount.value if document.total_amount else None,
            "items": [
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "total_price": item.total_amount,
                }
                for item in document.line_items
            ],
            "confidence": document.confidence,
        }
