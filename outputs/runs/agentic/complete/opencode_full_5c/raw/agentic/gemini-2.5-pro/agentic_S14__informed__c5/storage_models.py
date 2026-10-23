from typing import TypedDict


class BlobMetadata(TypedDict):
    name: str
    bucket: str
    size: int
    content_type: str
    updated: str
