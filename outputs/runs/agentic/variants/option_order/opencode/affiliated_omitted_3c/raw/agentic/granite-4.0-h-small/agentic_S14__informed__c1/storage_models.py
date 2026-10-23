from typing import List, Dict, Any

class ObjectMetadata:
    """Normalization helpers for Object metadata responses."""
    
    @staticmethod
    def from_s3(response: Dict[str, Any]) -> Dict[str, Any]:
        """Map boto3 HeadObject response to a consistent dict."""
        return {
            "ETag": response.get("ETag").strip('"'),
            "LastModified": response.get("LastModified"),
            "Size": response.get("ContentLength"),
            "ContentType": response.get("ContentType"),
            "StorageClass": response.get("StorageClass"),
        }

    @staticmethod
def from_b2(response: Dict[str, Any]) -> Dict[str, Any]:
        """Map Backblaze B2 API response to a consistent dict."""
        return {
            "fileName": response.get("fileName"),
            "size": response.get("size"),
            "uploadTimestamp": response.get("uploadTimestamp"),
            "contentType": response.get("contentType"),
        }
