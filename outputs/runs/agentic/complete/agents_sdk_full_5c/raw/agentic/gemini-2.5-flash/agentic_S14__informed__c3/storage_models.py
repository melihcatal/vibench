from typing import List, Dict, Any, Optional

class ObjectMetadata:
    key: str
    size: int
    last_modified: str
    e_tag: str
    content_type: Optional[str]
    metadata: Optional[Dict[str, str]]

    def __init__(self, key: str, size: int, last_modified: str, e_tag: str, content_type: Optional[str] = None, metadata: Optional[Dict[str, str]] = None):
        self.key = key
        self.size = size
        self.last_modified = last_modified
        self.e_tag = e_tag
        self.content_type = content_type
        self.metadata = metadata

class ObjectListing:
    objects: List[ObjectMetadata]
    next_continuation_token: Optional[str]

    def __init__(self, objects: List[ObjectMetadata], next_continuation_token: Optional[str] = None):
        self.objects = objects
        self.next_continuation_token = next_continuation_token
