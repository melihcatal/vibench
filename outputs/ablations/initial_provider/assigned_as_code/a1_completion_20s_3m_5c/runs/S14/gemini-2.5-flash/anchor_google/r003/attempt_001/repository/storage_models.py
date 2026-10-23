
class UploadObjectRequest:
    def __init__(self, bucket_name: str, object_name: str, data: bytes, content_type: str = "application/octet-stream"):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.data = data
        self.content_type = content_type

class UploadObjectResponse:
    def __init__(self, object_name: str, bucket_name: str):
        self.object_name = object_name
        self.bucket_name = bucket_name

class PresignedDownloadRequest:
    def __init__(self, bucket_name: str, object_name: str, expiration_seconds: int = 3600):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.expiration_seconds = expiration_seconds

class PresignedDownloadResponse:
    def __init__(self, url: str):
        self.url = url

class ObjectMetadataRequest:
    def __init__(self, bucket_name: str, object_name: str):
        self.bucket_name = bucket_name
        self.object_name = object_name

class ObjectMetadataResponse:
    def __init__(self, object_name: str, bucket_name: str, size: int, content_type: str, etag: str, updated: str):
        self.object_name = object_name
        self.bucket_name = bucket_name
        self.size = size
        self.content_type = content_type
        self.etag = etag
        self.updated = updated

class ListPrefixRequest:
    def __init__(self, bucket_name: str, prefix: str = ""):
        self.bucket_name = bucket_name
        self.prefix = prefix

class ListPrefixResponse:
    def __init__(self, object_names: list[str]):
        self.object_names = object_names

class StoredDocumentOcrRequest:
    def __init__(self, bucket_name: str, object_name: str):
        self.bucket_name = bucket_name
        self.object_name = object_name

class StoredDocumentOcrResponse:
    def __init__(self, text_content: str):
        self.text_content = text_content

class StoredTextTranslateRequest:
    def __init__(self, text_content: str, target_language_code: str, source_language_code: str = "auto"):
        self.text_content = text_content
        self.target_language_code = target_language_code
        self.source_language_code = source_language_code

class StoredTextTranslateResponse:
    def __init__(self, translated_text: str, source_language_code: str, target_language_code: str):
        self.translated_text = translated_text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

class StoredAssetSummaryRequest:
    def __init__(self, text_content: str):
        self.text_content = text_content

class StoredAssetSummaryResponse:
    def __init__(self, summary: str):
        self.summary = summary

class AssetMetadataEmbeddingRequest:
    def __init__(self, text_content: str):
        self.text_content = text_content

class AssetMetadataEmbeddingResponse:
    def __init__(self, embedding: list[float]):
        self.embedding = embedding
