from typing import TypedDict, Dict, Any, List


class ObjectMetadata(TypedDict):
    Bucket: str
    Key: str
    Size: int
    ETag: str
    LastModified: str  # ISO8601 string
    StorageClass: str


class ListResponse(TypedDict):
    Contents: List[ObjectMetadata]
    CommonPrefixes: List[str]


class OCRResult(TypedDict):
    text: str
    confidence: float


class TranslationResult(TypedDict):
    translated_text: str
    detected_source_language: str


class AssetSummary(TypedDict):
    title: str
    summary: str
    keywords: List[str]
