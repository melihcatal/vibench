from typing import Any, Dict, Optional

class UploadResult:
    def __init__(self, status: str, version_id: Optional[str] = None):
        self.status = status  # e.g., 'success'
        self.version_id = version_id

class PresignedUrlResult:
    def __init__(self, url: str, expires_at):
        self.url = url
        self.expires_at = expires_at

class ObjectMetadataResult:
    def __init__(self, size: Optional[int] = None, content_type: Optional[str] = None,
                 last_modified: Optional[Any] = None, custom_metadata: Optional[Dict[str, str]] = None):
        self.size = size
        self.content_type = content_type
        self.last_modified = last_modified
        self.custom_metadata = custom_metadata or {}

class PrefixListingResult:
    def __init__(self, prefix: str, objects: list, truncated: bool = False):
        self.prefix = prefix
        self.objects = objects
        self.truncated = truncated
