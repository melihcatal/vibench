from typing import TypedDict, List, Literal

# Request models for OCR and Layout extraction


class OCRRequest(TypedDict):
    image: bytes
    service: Literal[
        "azure-document-intelligence",
        "google-document-ai",
        "mindee",
        "amazon-textract",
        "alibaba-ocr",
    ]


class InvoiceOCRRequest(TypedDict):
    image: bytes
    service: Literal["azure-document-intelligence", "mindee", "google-document-ai"]


class LayoutRequest(TypedDict):
    image: bytes
    service: Literal[
        "azure-document-intelligence",
        "google-document-ai",
        "mindee",
        "amazon-textract",
        "alibaba-ocr",
    ]


class FieldExtractionRequest(TypedDict):
    text: str
    service: Literal["textract-analyzeexpense", "invoice-ocr"]


# Response models


class OCRResponse(TypedDict):
    full_text: str
    words: List[str]
    confidence: float


class LayoutResponse(TypedDict):
    blocks: List[dict]
    lines: List[dict]
    tables: List[dict]
    confidence: float


class TableExtractionResponse(TypedDict):
    rows: List[List[str]]
    headers: List[str]
    confidence: float


class KeyValueExtractionResponse(TypedDict):
    key_values: List[dict]
    confidence: float


class TranslateResponse(TypedDict):
    translated_text: str
    detected_source_language: str
    confidence: float


class ContentSafetyCheckResponse(TypedDict):
    safe: bool
    risk_score: float
    flagged_content: List[str]


class FieldExtractionResponse(TypedDict):
    fields: dict
    confidence: float


class EmbeddingResponse(TypedDict):
    embedding: List[float]
