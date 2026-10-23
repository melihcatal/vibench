from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class S3ObjectInfo:
    key: str
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    size: Optional[int] = None
    storage_class: Optional[str] = None

@dataclass
class DocumentTextractJobStatus:
    job_id: str
    status: str # e.g., SUCCEEDED, FAILED, IN_PROGRESS
    warnings: List[Dict[str, Any]] = field(default_factory=list)
    status_message: Optional[str] = None

@dataclass
class TranslatedTextResult:
    translated_text: str
    source_language_code: str
    target_language_code: str

@dataclass
class EmbeddedVector:
    vector: List[float]
    input_text: str
    model_id: str

# More models can be added here as needed for specific request/response payloads.
