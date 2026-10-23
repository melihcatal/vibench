from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import datetime

@dataclass
class ObjectInfo:
    """Represents basic information about a stored object."""
    key: str
    size: int
    last_modified: datetime.datetime
    etag: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)

@dataclass
class DocumentText:
    """Represents extracted text from a document."""
    text: str
    source_language: Optional[str] = None
    
@dataclass
class TranslatedText:
    """Represents translated text."""
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class DocumentSummary:
    """Represents a summary of a document."""
    summary_text: str
    source_model: Optional[str] = None

@dataclass
class EmbeddingVector:
    """Represents a vector embedding."""
    vector: List[float]
    model_id: str
    input_text: Optional[str] = None

@dataclass
class PresignedUrl:
    """Represents a presigned URL for an object."""
    url: str
    expiration_seconds: int
    object_key: str

if __name__ == '__main__':
    # Example usage (not executed by the system)
    # obj_info = ObjectInfo(key="my-doc.pdf", size=1024, last_modified=datetime.datetime.now())
    # print(obj_info)
    # translated = TranslatedText(translated_text="Hello", source_language="en", target_language="es")
    # print(translated)
    pass
