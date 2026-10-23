from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class S3UploadResult:
    bucket: str
    key: str
    version_id: Optional[str] = None

@dataclass
class S3PresignResult:
    url: str
    expiration: int

@dataclass
class S3HeadObjectResult:
    bucket: str
    key: str
    metadata: Dict[str, Any]

@dataclass
class S3Summary:
    key: str
    size: Optional[int] = None
    last_modified: Optional[Any] = None

@dataclass
class S3ListResult:
    bucket: str
    prefix: str
    delimiter: Optional[str] = None
    items: list[S3Summary] = None

@dataclass
class OCRResult:
    text: str
    language: str = 'en'

@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class MetadataEmbeddingResult:
    metadata: dict
    embedding: list[float]

@dataclass
class TextEmbeddingResult:
    text: str
    embedding: list[float]
