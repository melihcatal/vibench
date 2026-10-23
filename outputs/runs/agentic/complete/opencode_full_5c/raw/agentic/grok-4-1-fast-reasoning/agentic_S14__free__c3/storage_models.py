from typing import List, Dict, Any


def extract_keys(contents: List[Dict[str, Any]]) -> List[str]:
    return [obj["Key"] for obj in contents if "Key" in obj]


def head_object_to_metadata(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "content_length": response.get("ContentLength"),
        "content_type": response.get("ContentType"),
        "last_modified": str(response.get("LastModified")),
        "etag": response.get("ETag"),
        "metadata": dict(response.get("Metadata", {})),
    }
