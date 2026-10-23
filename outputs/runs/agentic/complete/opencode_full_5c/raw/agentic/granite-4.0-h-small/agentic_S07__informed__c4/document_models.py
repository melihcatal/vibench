from __future__ import annotations
from typing import Any, Dict, List, Optional

# -----------------------------------------------------------------------
# Request models
# -----------------------------------------------------------------------


class DocumentRequest:
    """
    Base request for document processing.
    """

    def __init__(self, gcs_uri: str, **kwargs):
        self.gcs_uri = gcs_uri
        # Additional optional attributes
        self.metadata = kwargs.get("metadata", None)
        self.client_options = kwargs.get("client_options", None)
        self.raw_response = kwargs.get("raw_response", False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gcs_uri": self.gcs_uri,
            "metadata": self.metadata,
            "client_options": self.client_options,
            "raw_response": self.raw_response,
        }


# -----------------------------------------------------------------------
# Response / Normalization models
# -----------------------------------------------------------------------


class ExtractedText:
    """
    Normalized output for plain text extraction.
    """

    def __init__(self, text: str, confidence: Optional[float] = None):
        self.text = text
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "confidence": self.confidence}


class LayoutBlock:
    """
    Normalized layout block representation.
    """

    def __init__(
        self,
        type_: str,
        page: int,
        bbox: List[float],
        text: str,
        confidence: Optional[float] = None,
    ):
        self.type = type_  # e.g., 'BLOCK', 'PARAGRAPH', 'LINE'
        self.page = page  # 0-indexed page number
        self.bbox = bbox  # [x, y, width, height] normalized coordinates [0, 1]
        self.text = text
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "page": self.page,
            "bbox": self.bbox,
            "text": self.text,
            "confidence": self.confidence,
        }


class LayoutLine:
    """
    Normalized line layout.
    """

    def __init__(
        self,
        type_: str,
        page: int,
        bbox: List[float],
        text: str,
        confidence: Optional[float] = None,
    ):
        self.type = type_
        self.page = page
        self.bbox = bbox
        self.text = text
        self.confidence = confidence

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "page": self.page,
            "bbox": self.bbox,
            "text": self.text,
            "confidence": self.confidence,
        }


class LayoutTable:
    """
    Normalized table information.
    """

    def __init__(self, header: List[str], rows: List[List[str]]):
        self.header = header
        self.rows = rows

    def to_dict(self) -> Dict[str, Any]:
        return {"header": self.header, "rows": self.rows}


class ExtractedTable:
    """
    Normalized table extraction.
    """

    def __init__(self, header: List[str], rows: List[List[str]]):
        self.header = header
        self.rows = rows

    def to_dict(self) -> Dict[str, Any]:
        return {"header": self.header, "rows": self.rows}


class KeyValuePair:
    """
    Normalized key-value pair from form-like documents.
    """

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def to_dict(self) -> Dict[str, Any]:
        return {"key": self.key, "value": self.value}


# -----------------------------------------------------------------------
# Normalization helpers (simple converters from provider-specific objects to normalized classes)
# -----------------------------------------------------------------------


def normalize_text(provider_response: Dict[str, Any]) -> ExtractedText:
    """Convert generic provider text output to ExtractedText."""
    return ExtractedText(
        provider_response.get("text", ""), provider_response.get("confidence")
    )


def normalize_layout(provider_response: Dict[str, Any]) -> Dict[str, List[LayoutBlock]]:
    """Convert layout output to list of LayoutBlock."""
    blocks = [
        LayoutBlock(
            l.type, l.page, l.bounding_poly.normalized_vertices, l.text, l.confidence
        )
        for l in provider_response.get("blocks", [])
    ]
    lines = [
        LayoutLine(
            l.type, l.page, l.bounding_poly.normalized_vertices, l.text, l.confidence
        )
        for l in provider_response.get("lines", [])
    ]
    tables = [
        LayoutTable(t.header, t.rows) for t in provider_response.get("tables", [])
    ]
    return {"blocks": blocks, "lines": lines, "tables": tables}


# -----------------------------------------------------------------------
# Utility helpers
# -----------------------------------------------------------------------
def load_credentials(service_name: str) -> Dict[str, str]:
    """Load required environment variables for the given service."""
    required = {
        "Google Document AI": ["GOOGLE_APPLICATION_CREDENTIALS"],
        "Mindee": ["MINDEE_API_KEY"],
        "Amazon Textract": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        "Alibaba Cloud OCR": [
            "ALIBABA_CLOUD_ACCESS_KEY_ID",
            "ALIBABA_CLOUD_ACCESS_KEY_SECRET",
        ],
        "Azure Document Intelligence": [
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
            "AZURE_DOCUMENT_INTELLIGENCE_KEY",
        ],
    }
    return {env: os.getenv(env) for env in required.get(service_name, [])}


def example_credentials_check(service_name: str) -> bool:
    """Very simple check whether all required environment variables are set."""
    creds = load_credentials(service_name)
    return all(creds.values())


if __name__ == "__main__":
    # Quick sanity check
    creds = load_credentials("Google Document AI")
    print("Google Document AI credentials loaded:", creds)
