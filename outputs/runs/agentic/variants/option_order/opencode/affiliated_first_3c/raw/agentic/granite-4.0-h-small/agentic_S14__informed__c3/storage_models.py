from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class UploadRequest:
    """Payload for uploading a file or byte stream."""
    bucket_name: str
    key: str          # object path
    data: bytes       # raw content
    content_type: Optional[str] = None

@dataclass
class DownloadPresignRequest:
    """Input for generating a presigned download URL."""
    bucket_name: str
    key: str
    expires_in_seconds: int = 3600  # 1 hour

@dataclass
class ObjectMetadataResponse:
    """Normalized metadata returned from the storage provider."""
    bucket: str
    key: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    content_type: Optional[str] = None
    # Additional fields can be added as needed

@dataclass
class ListObjectsResult:
    """Result of a prefix/list operation."""
    bucket: str
    prefix: str
    delimiter: Optional[str] = None
    contents: Optional[list] = None
    common_prefixes: Optional[list] = None

# Helper for OCR step - normalization of OCR response
class OCRResponse:
    """Placeholder for OCR tool output normalization."""
    def __init__(self, raw): self.raw = raw
    @property
def text(self) -> str:
        # Extract plain text from provider‑specific structure
        # Placeholder: assume raw contains a 'text' field
        return self.raw.get('text', '')

# Helper for translation step
@dataclass
class TranslateRequest:
    """Text to translate extracted from a document."""
    source_text: str
    target_language: str = "en"

@dataclass
class TranslateResponse:
    """Translation result."""
    translated_text: str

# Helper for summarization step
@dataclass
class SummarizeRequest:
    """Content extracted from a stored asset."""
    content: str
    max_target_length: int = 200

@dataclass
class SummarizeResponse:
    """Generated summary."""
    summary: str

# Helper for embedding/metadata enrichment
@dataclass
class EmbedRequest:
    """Data for embedding metadata + extracted text."""
    metadata: Dict[str, Any]
    extracted_text: str

@dataclass
class EmbedResponse:
    """Embedding vectors plus metadata for search index."""
    vector: list[float]   # flattened embedding
    metadata: Dict[str, Any]
