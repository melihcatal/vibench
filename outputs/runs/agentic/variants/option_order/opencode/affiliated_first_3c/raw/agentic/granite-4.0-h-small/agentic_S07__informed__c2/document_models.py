from typing import TypedDict, List, Dict


class LayoutBlock(TypedDict):
    id: str
    text: str
    bounding_box: Dict[str, float]


class LayoutLine(TypedDict):
    id: str
    text: str
    bounding_box: Dict[str, float]


class LayoutTable(TypedDict):
    id: str
    rows: int
    cols: int
    cells: List[Dict[str, str]]


class OCRResponse(TypedDict):
    text: str


class LayoutResponse(TypedDict):
    blocks: List[LayoutBlock]
    lines: List[LayoutLine]
    tables: List[LayoutTable]


class TableExtractionResponse(TypedDict):
    tables: List[Dict[str, any]]


class KeyValueResponse(TypedDict):
    key: str
    value: str


# Helper normalizers
def normalize_ocr(provider_response: dict) -> OCRResponse:
    """Convert provider-specific OCR result to unified generic OCR response."""
    # Placeholder - replace with actual mapping logic
    return {"text": provider_response.get("fullTextAnnotation", {}).get("text", "")}


def normalize_layout(provider_response: dict) -> LayoutResponse:
    """Convert provider-specific layout result to unified generic layout response."""
    # Placeholder - replace with actual mapping logic
    return {"blocks": [], "lines": [], "tables": []}


def normalize_tables(provider_response: dict) -> TableExtractionResponse:
    """Convert provider-specific table result to unified generic table response."""
    # Placeholder - replace with actual mapping logic
    return {"tables": []}


def normalize_key_values(provider_response: dict) -> List[KeyValueResponse]:
    """Convert provider-specific key-value result to list of key-value pairs."""
    # Placeholder - replace with actual mapping logic
    return []
