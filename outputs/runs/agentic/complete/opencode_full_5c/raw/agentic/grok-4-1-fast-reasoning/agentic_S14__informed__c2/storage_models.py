from typing import TypedDict, Dict, Any, List, Optional

class UploadResponse(TypedDict):
    etag: str
    version_id: Optional[str]

class ObjectMetadata(TypedDict):
    content_length: int
    content_type: Optional[str]
    last_modified: str
    etag: str
    metadata: Dict[str, str]

class ListObjectsResponse(TypedDict):
    contents: List[str]
    common_prefixes: List[str]

def normalize_metadata(raw_head: Dict[str, Any]) -&gt; ObjectMetadata:
    return {
        'content_length': raw_head['ContentLength'],
        'content_type': raw_head.get('ContentType'),
        'last_modified': raw_head['LastModified'].isoformat(),
        'etag': raw_head['ETag'].strip('"'),
        'metadata': dict(raw_head.get('Metadata', {}))
    }