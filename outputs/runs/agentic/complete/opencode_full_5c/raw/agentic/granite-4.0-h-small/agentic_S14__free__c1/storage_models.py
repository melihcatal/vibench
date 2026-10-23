# storage_models.py
# [HELPER] Request/response and normalization helpers for Managed Object Storage
from typing import Dict, Any, Optional, Union, BinaryIO

# Standardized request payload models (simple dicts for this demo)
UploadRequest = Dict[str, Union[str, bytes]]


# Normalized response structures used across integration files
class UploadResponse:
    def __init__(self, **kwargs: Any):
        self.__dict__.update(kwargs)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


class DownloadResponse:
    def __init__(self, url: Optional[str] = None, **extra: Any):
        self.url = url
        self.extra = extra

    def to_dict(self) -> Dict[str, Any]:
        return {**self.__dict__}


class ObjectMetadataResponse:
    def __init__(self, **metadata: Any):
        self.__dict__.update(metadata)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


class ListResponse:
    def __init__(self, contents: Optional[List[Dict[str, Any]]] = None, **paging: Any):
        self.contents = contents or []
        self.paging = paging

    def to_dict(self) -> Dict[str, Any]:
        return {"contents": self.contents, **self.paging}


# Helper to normalize raw S3 responses into our models


def normalize_upload_response(raw: Dict[str, Any]) -> UploadResponse:
    return UploadResponse(**raw)


def normalize_download_response(
    url: Optional[str] = None, extra: Dict[str, Any] = None
) -> DownloadResponse:
    return DownloadResponse(url=url, **(extra or {}))


def normalize_metadata_response(raw: Dict[str, Any]) -> ObjectMetadataResponse:
    return ObjectMetadataResponse(**raw)


def normalize_list_response(raw: Dict[str, Any]) -> ListResponse:
    return ListResponse(contents=raw.get("Contents", []), **raw)
