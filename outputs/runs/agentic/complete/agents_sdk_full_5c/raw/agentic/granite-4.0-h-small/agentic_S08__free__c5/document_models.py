from typing import List, Dict, Any

class InvoiceExtractionRequest:
    """Encapsulate a document and extraction parameters for an invoice."""
    def __init__(self, document: bytes, document_type: str = "invoice") -> None:
        self.document = document  # raw bytes (PDF, image, etc.)
        self.document_type = document_type
        self.service = "textract"  # provider identifier

    def to_dict(self) -> Dict[str, Any]:
        """Prepare payload for Textract synchronous API."""
        return {
            "Document": {
                "Bytes": self.document
            },
            # Textract expects 'DocumentType' for more control; omitted for brevity
        }

class InvoiceExtractionResponse:
    """Normalized response structure for invoice extraction."""
    def __init__(self, raw_response: Any) -> None:
        self.raw = raw_response
        # Example mapping to our own fields:
        self.vendor = self._extract_vendor(raw_response)
        self.date = self._extract_date(raw_response)
        self.total = self._extract_total(raw_response)
        self.line_items = self._extract_line_items(raw_response)

    def _extract_vendor(self, response: Any) -> str:
        # Textract does not have a dedicated vendor field; placeholder heuristic
        return "Acme Corp"
    
    def _extract_date(self, response: Any) -> str:
        # Placeholder: find a date pattern in the response
        return "2023-07-15"
    
    def _extract_total(self, response: Any) -> float:
        # Placeholder: sum amounts or locate a total line
        return 123.45
    
    def _extract_line_items(self, response: Any) -> List[Dict[str, Any]]:
        # Placeholder: return a list of dicts with description, quantity, price
        return [
            {"description": "Office Supplies", "quantity": 1, "unit_price": 50.0, "amount": 50.0},
            {"description": "Software License", "quantity": 1, "unit_price": 73.45, "amount": 73.45}
        ]

class ReceiptExtractionRequest(InvoiceExtractionRequest):
    """Re-use same model for receipts (inheritance)."""
    pass

class ReceiptExtractionResponse(InvoiceExtractionResponse):
    """Re-use same response model for receipts."""
    def __init__(self, raw_response: Any) -> None:
        super().__init__(raw_response)


class NormalizedExpenseRequest:
    """Create a request payload for normalization step."""
    def __init__(self, extracted: Dict[str, Any]) -> None:
        self.extracted = extracted

class NormalizedExpenseResponse:
    """Encapsulate the normalized expense record."""
    def __init__(self, expense: Dict[str, Any]) -> None:
        self.expense = expense