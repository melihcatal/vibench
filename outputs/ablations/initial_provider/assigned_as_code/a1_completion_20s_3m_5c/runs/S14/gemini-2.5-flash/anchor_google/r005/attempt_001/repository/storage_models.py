from typing import Dict, Any

class UploadObjectPayload:
    object_name: str
    data: bytes
    content_type: str

class PresignedURLResponse:
    url: str

class ObjectMetadataResponse:
    object_name: str
    size: int
    content_type: str
    updated: str

class ListPrefixResponse:
    objects: list[Dict[str, Any]]
