from typing import Dict, Any, Optional
import os
from mindee import Client, documents
from mindee.input import LocalInputSource
from mindee.errors import MindeeException


class InvoiceExtractor:
    def __init__(self):
        self.mindee_client = Client(api_key=os.getenv("MINDEE_API_KEY"))

    def extract(self, file_path: str) -> Dict[str, Any]:
        try:
            input_source = LocalInputSource(file_path)
            response = self.mindee_client.parse(
                documents.TypeInvoiceV4, input_source=input_source
            )
            return self._normalize_response(response.document)
        except MindeeException as e:
            raise Exception(f"Mindee Invoice extraction failed: {str(e)}")

    def _normalize_response(
        self, document: documents.InvoiceV4Document
    ) -> Dict[str, Any]:
        return {
            "vendor": document.supplier.name.value if document.supplier else None,
            "date": document.date.value.isoformat() if document.date else None,
            "total": document.total_amount.value if document.total_amount else None,
            "line_items": [
                {
                    "description": line.description,
                    "quantity": line.quantity,
                    "unit_price": line.unit_price,
                    "total_price": line.total_amount,
                }
                for line in document.line_items
            ],
            "confidence": document.confidence,
        }
