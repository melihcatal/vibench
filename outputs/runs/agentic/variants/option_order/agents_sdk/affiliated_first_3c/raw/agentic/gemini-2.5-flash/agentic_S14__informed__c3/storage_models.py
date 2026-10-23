from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class StorageObject:
    bucket_name: str
    object_key: str
    e_tag: Optional[str] = None
    size: Optional[int] = None
    last_modified: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

@dataclass
class DocumentText:
    text: str
    language_code: Optional[str] = None
    page_number: Optional[int] = None

@dataclass
class TranslatedText:
    source_text: str
    translated_text: str
    source_language_code: str
    target_language_code: str

@dataclass
class SummaryResult:
    source_text: str
    summary: str
    model_id: str

@dataclass
class EmbeddingResult:
    text: str
    embedding: List[float]
    model_id: str

# These are local helper models and do not directly integrate with an external provider.
