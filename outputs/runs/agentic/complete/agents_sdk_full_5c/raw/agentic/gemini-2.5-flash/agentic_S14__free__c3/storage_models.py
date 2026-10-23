from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List, Optional

@dataclass
class ObjectSummary:
    """Summary information for an S3 object."""
    key: str
    last_modified: datetime
    size: int
    e_tag: str
    storage_class: str

@dataclass
class ObjectMetadata:
    """
    Detailed metadata for an S3 object (from head_object).
    Note: Not all fields may be present for every object.
    """
    key: str
    last_modified: Optional[datetime] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    e_tag: Optional[str] = None
    storage_class: Optional[str] = None
    user_metadata: Dict[str, str] = None

@dataclass
class DocumentTextractResult:
    """
    Represents the output from AWS Textract for document analysis.
    """
    job_id: Optional[str] = None
    status: Optional[str] = None
    detected_text: Optional[str] = None
    pages: Optional[List[str]] = None
    full_response: Optional[Dict[str, Any]] = None # Store the raw response if needed

@dataclass
class TranslatedTextResult:
    """
    Represents the output from AWS Translate.
    """
    source_language_code: str
    target_language_code: str
    translated_text: str
    # Raw response could be added here if needed

@dataclass
class AssetSummaryResult:
    """
    Represents the summarization output from a model like Bedrock/Claude.
    """
    summary_text: str
    # Raw response could be added here if needed

@dataclass
class EmbeddingResult:
    """
    Represents the embedding output from a model like Bedrock/Titan Embeddings.
    """
    embedding: List[float]
    model_id: str
    input_text: str
