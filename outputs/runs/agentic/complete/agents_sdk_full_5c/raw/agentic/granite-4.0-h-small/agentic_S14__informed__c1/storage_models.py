from dataclasses import dataclass

class StorageObject:
    """Normalized object metadata returned by list and head operations."""
    @dataclass
    class Size:
        bytes: int
    
    def __init__(self, key: str, size: Size, last_modified: str, etag: str, storage_class: str):
        self.key = key
        self.size = size
        self.last_modified = last_modified
        self.etag = etag
        self.storage_class = storage_class
    
    @staticmethod
def from_dict(source: Dict[str, Any]) -> 'StorageObject':
        return StorageObject(
            key=source.get('Key'),
            size=StorageObject.Size(bytes=source.get('Size')),
            last_modified=source.get('LastModified'),
            etag=source.get('ETag'),
            storage_class=source.get('StorageClass')
        )

# Example request container for upload
@dataclass
class UploadRequest:
    bucket: str
    key: str
    body: bytes
    content_type: str = 'application/octet-stream'

# Normalized list response
@dataclass
class ListResult:
    contents: list[StorageObject] = field(default_factory=list)
    prefixes: list[str] = field(default_factory=list)

# Placeholder for OCR result (used by later step files)
@dataclass
class OcrResult:
    text: str
    regions: list[Dict[str, Any]] = field(default_factory=list)

# Placeholder for embedding result
@dataclass
class Embedding:
    vector: list[float]
