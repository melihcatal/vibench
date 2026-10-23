import dataclasses
from typing import Dict, List, Optional


@dataclasses.dataclass
class UploadObjectRequest:
    bucket_name: str
    object_key: str
    data: bytes


@dataclasses.dataclass
class UploadObjectResponse:
    e_tag: str
    version_id: Optional[str] = None


@dataclasses.dataclass
class DownloadUrlResponse:
    presigned_url: str


@dataclasses.dataclass
class ObjectMetadataResponse:
    content_length: int
    content_type: str
    last_modified: str
    e_tag: str
    metadata: Dict[str, str]


@dataclasses.dataclass
class ObjectSummary:
    key: str
    last_modified: str
    e_tag: str
    size: int


@dataclasses.dataclass
class ListObjectsResponse:
    objects: List[ObjectSummary]
    next_continuation_token: Optional[str] = None


@dataclasses.dataclass
class OcrResult:
    extracted_text: str


@dataclasses.dataclass
class TranslatedTextResult:
    translated_text: str


@dataclasses.dataclass
class SummaryResult:
    summary_text: str


@dataclasses.dataclass
class EmbeddingResult:
    embedding: List[float]
