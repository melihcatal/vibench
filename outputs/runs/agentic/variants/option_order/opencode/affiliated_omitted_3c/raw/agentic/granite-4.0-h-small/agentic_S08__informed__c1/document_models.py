# [HELPER] document_models.py
# Define local request, response, and normalization helpers for Structured Document Extraction

from __future__ import annotations
from typing import Any, Dict, List


# ---------- Request Payload Model ----------
class ExtractionRequest:
    def __init__(self, provider: str, image_bytes: bytes):
        self.provider = provider
        self.image_bytes = image_bytes
        self.payload: Dict[str, Any] = build_extraction_payload(provider, image_bytes)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "payload": self.payload,
        }


# ---------- Response Models ----------
class InvoiceResponse:
    def __init__(
        self,
        vendor: str = "",
        date: str = "",
        total: float = 0.0,
        line_items: List[Dict[str, Any]] = None,
    ):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.line_items = line_items or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vendor": self.vendor,
            "date": self.date,
            "total": self.total,
            "line_items": self.line_items,
        }


class ReceiptResponse(InvoiceResponse):
    pass


# ---------- Normalization ----------
NORMALIZED_SCHEMA = {
    "vendor",
    "date",
    "total",
    "line_items",
    "merchant",
    "tax",
    "items",
}


def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure the record contains all schema fields, filling missing ones with defaults.
    This is a shallow normalization suitable for downstream processing.
    """
    normalized = {k: record.get(k, None) for k in NORMALIZED_SCHEMA}
    # Basic type enforcement
    normalized["vendor"] = str(normalized["vendor"] or "")
    normalized["date"] = str(normalized["date"] or "")
    normalized["total"] = float(normalized["total"] or 0)
    if normalized["line_items"] is None:
        normalized["line_items"] = []
    if isinstance(normalized["line_items"], list):
        pass
    elif isinstance(normalized["line_items"], dict):
        # Some providers return a list in a wrapper dict
        normalized["line_items"] = [normalized["line_items"]]
    normalized["merchant"] = str(normalized["merchant"] or "")
    normalized["tax"] = float(normalized["tax"] or 0)
    if normalized["items"] is None:
        normalized["items"] = []
    return normalized


# ---------- Utility ----------
VALID_REQ_FIELDS = {"provider": str, "image_bytes": bytes}


def validate_extraction_request(req: ExtractionRequest) -> bool:
    """Validate that the request contains required fields and correct types."""
    for field, expected_type in VALID_REQ_FIELDS.items():
        value = getattr(req, field)
        if not isinstance(value, expected_type):
            return False
    return True


if __name__ == "__main__":
    # Example usage
    import base64

    test_image = base64.b64encode(b"dummy image data").decode("utf-8")
    req = ExtractionRequest(provider="mindee", image_bytes=base64.b64decode(test_image))  # type: ignore
    print("ExtractionRequest ready:", req.to_dict())
