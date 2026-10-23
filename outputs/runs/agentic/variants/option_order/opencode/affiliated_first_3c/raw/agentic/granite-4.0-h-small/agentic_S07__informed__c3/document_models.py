from typing import Any, Dict, List, Optional

# ---------- Generic request/response models ----------


class DocumentRequest:
    """Local model for the generic document extraction request."""

    def __init__(
        self,
        image_path: str,
        provider: str = "mindee",
        product: Optional[str] = None,
    ):
        self.image_path = image_path
        self.provider = provider
        self.product = product  # e.g. "generic", "layout", "form", "table"


class DocumentResponse:
    """Normalized response shape used internally for further steps."""

    def __init__(self):
        self.text: str = ""
        self.layout: List[Any] = []
        self.tables: List[Any] = []
        self.fields: List[Dict[str, Any]] = []

    def from_raw(self, raw: Dict[str, Any]):
        """Copy fields from provider‑specific raw dict to the unified model."""
        self.text = raw.get("text", "")
        self.layout = raw.get("blocks", [])  # generic layout blocks
        self.tables = raw.get("tables", [])
        self.fields = raw.get("fields", [])


# ---------- Helper functions for downstream steps ----------
class KeyValueCollection:
    """Collection of extracted key‑value pairs.
    Represents a simple dict after extraction."""

    def __init__(self, kv_dict: Dict[str, str]):
        self.data = kv_dict

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self.data.get(key, default)


# ---------- Example usage ----------
if __name__ == "__main__":
    # Simulate a normalised response
    sample_response = {
        "text": "Sample document OCR",
        "layout": ["block1", "block2"],
        "tables": ["tableA"],
        "fields": [{"key": "Name", "value": "John"}],
    }
    dr = DocumentResponse()
    dr.from_raw(sample_response)
    kv = KeyValueCollection({"Name": "John"})
    print("Extracted name:", kv.get("Name"))
