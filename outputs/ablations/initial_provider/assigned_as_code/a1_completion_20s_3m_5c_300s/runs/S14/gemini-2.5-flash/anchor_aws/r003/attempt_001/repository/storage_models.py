from typing import Dict, Any, Optional


def UploadObjectPayload(object_name: str, data: Any, content_type: Optional[str] = None) -> Dict[str, Any]:
    payload = {"object_name": object_name, "data": data}
    if content_type:
        payload["content_type"] = content_type
    return payload


def UploadObjectResponse(object_name: str) -> Dict[str, str]:
    return {"object_name": object_name}


def PresignedDownloadPayload(object_name: str, expiration_seconds: int = 3600) -> Dict[str, Any]:
    return {"object_name": object_name, "expiration_seconds": expiration_seconds}


def PresignedDownloadResponse(object_name: str, url: str) -> Dict[str, str]:
    return {"object_name": object_name, "url": url}


def ObjectMetadataPayload(object_name: str) -> Dict[str, str]:
    return {"object_name": object_name}


def ObjectMetadataResponse(object_name: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    return {"object_name": object_name, "metadata": metadata}


def ListPrefixPayload(prefix: str, max_keys: int = 100) -> Dict[str, Any]:
    return {"prefix": prefix, "max_keys": max_keys}


def ListPrefixResponse(prefix: str, objects: list) -> Dict[str, Any]:
    return {"prefix": prefix, "objects": objects}
