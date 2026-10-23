from typing import Dict, Any, List, Optional
from datetime import datetime

class S3ObjectMetadata:
    def __init__(
        self, 
        key: str,
        last_modified: Optional[datetime] = None,
        size: Optional[int] = None,
        e_tag: Optional[str] = None,
        content_type: Optional[str] = None,
        user_metadata: Optional[Dict[str, str]] = None
    ):
        self.key = key
        self.last_modified = last_modified
        self.size = size
        self.e_tag = e_tag
        self.content_type = content_type
        self.user_metadata = user_metadata if user_metadata is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "last_modified": self.last_modified.isoformat() if self.last_modified else None,
            "size": self.size,
            "e_tag": self.e_tag,
            "content_type": self.content_type,
            "user_metadata": self.user_metadata
        }

class PresignedUrlResponse:
    def __init__(self, url: str, expiration_seconds: int):
        self.url = url
        self.expiration_seconds = expiration_seconds
    
    def to_dict(self) -> Dict[str, Any]:
        return {"url": self.url, "expiration_seconds": self.expiration_seconds}

class OCRResult:
    def __init__(self, text: str, detected_languages: Optional[List[str]] = None):
        self.text = text
        self.detected_languages = detected_languages if detected_languages is not None else []

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "detected_languages": self.detected_languages}

class TranslatedText:
    def __init__(self, text: str, detected_source_language: Optional[str] = None, target_language: str = "en"):
        self.text = text
        self.detected_source_language = detected_source_language
        self.target_language = target_language

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "detected_source_language": self.detected_source_language,
            "target_language": self.target_language
        }

class SummaryResult:
    def __init__(self, summary_text: str, model_used: str):
        self.summary_text = summary_text
        self.model_used = model_used
    
    def to_dict(self) -> Dict[str, Any]:
        return {"summary_text": self.summary_text, "model_used": self.model_used}

class EmbeddingResult:
    def __init__(self, embedding: List[float], model_used: str, original_text_hash: Optional[str] = None):
        self.embedding = embedding
        self.model_used = model_used
        self.original_text_hash = original_text_hash

    def to_dict(self) -> Dict[str, Any]:
        return {
            "embedding": self.embedding,
            "model_used": self.model_used,
            "original_text_hash": self.original_text_hash
        }
