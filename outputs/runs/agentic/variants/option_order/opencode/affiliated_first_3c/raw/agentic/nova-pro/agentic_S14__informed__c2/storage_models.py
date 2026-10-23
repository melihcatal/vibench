from typing import Dict, Any


class UploadResponse:
    def __init__(self, status: str, message: str):
        self.status = status
        self.message = message


class DownloadURL:
    def __init__(self, url: str):
        self.url = url


class ObjectMetadata:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata


class ObjectList:
    def __init__(self, objects: list):
        self.objects = objects
