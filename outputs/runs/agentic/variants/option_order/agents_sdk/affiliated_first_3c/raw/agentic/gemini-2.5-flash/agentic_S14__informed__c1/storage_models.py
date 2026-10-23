from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class StorageObject:
    bucket_name: str
    object_name: str

@dataclass
class UploadRequest:
    bucket_name: str
    object_name: str
    file_path: Optional[str] = None
    data: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

@dataclass
class OCRRequest:
    bucket_name: str
    object_name: str
    mime_type: str = "application/pdf"

@dataclass
class TranslationRequest:
    text_content: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class SummarizationRequest:
    text_content: str
    model_name: str = "gemini-pro"
    max_output_tokens: int = 200

@dataclass
class EmbeddingRequest:
    text_content: str
    model_name: str = "models/embedding-001"

