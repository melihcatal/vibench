from typing import Dict, Any, Optional
import os
from mindee import Client, PredictResponse, product


class ReceiptExtractor:
    def __init__(self):
        self.api_key = os.getenv("MINDEE_API_KEY")
        self.client = Client(api_key=self.api_key)

    def extract_receipt_fields(self, document_path: str) -> Dict[str, Any]:
        with open(document_path, "rb") as document:
            response: PredictResponse = self.client.parse(
                product.ReceiptV5, document=document
            )

        receipt_data = {
            "merchant": self._extract_merchant(response),
            "tax": self._extract_tax(response),
            "total": self._extract_total(response),
            "items": self._extract_items(response),
            "confidence": response.document.inference.prediction.confidence,
        }
        return receipt_data

    def _extract_merchant(self, response: PredictResponse) -> Optional[str]:
        merchant = response.document.inference.prediction.merchant_name.value
        return merchant if merchant else None

    def _extract_tax(self, response: PredictResponse) -> Optional[float]:
        tax = response.document.inference.prediction.taxes.value
        return float(tax[0].value) if tax and len(tax) > 0 else None

    def _extract_total(self, response: PredictResponse) -> Optional[float]:
        total = response.document.inference.prediction.total_amount.value
        return float(total) if total else None

    def _extract_items(self, response: PredictResponse) -> list[Dict[str, Any]]:
        items = []
        for item in response.document.inference.prediction.line_items:
            items.append(
                {
                    "description": item.description.value if item.description else None,
                    "amount": float(item.total_amount.value)
                    if item.total_amount
                    else None,
                }
            )
        return items
