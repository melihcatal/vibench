from typing import Dict, Any, List, Optional


class ObjectStorageConfig:
    def __init__(self, bucket_name: str, region_name: Optional[str] = None):
        self.bucket_name = bucket_name
        self.region_name = region_name


class UploadObjectPayload:
    def __init__(self, object_name: str, data: Any, content_type: Optional[str] = None):
        self.object_name = object_name
        self.data = data
        self.content_type = content_type


class UploadObjectResult:
    def __init__(self, object_name: str):
        self.object_name = object_name


class PresignedUrlResult:
    def __init__(self, url: str):
        self.url = url


class ObjectMetadataResult:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata


class ListObjectsResult:
    def __init__(self, object_names: List[str]):
        self.object_names = object_names


class OCRResult:
    def __init__(self, text: str):
        self.text = text


class TranslationResult:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text


class SummaryResult:
    def __init__(self, summary_text: str):
        self.summary_text = summary_text


class EmbeddingResult:
    def __init__(self, embedding: List[float]):
        self.embedding = embedding
