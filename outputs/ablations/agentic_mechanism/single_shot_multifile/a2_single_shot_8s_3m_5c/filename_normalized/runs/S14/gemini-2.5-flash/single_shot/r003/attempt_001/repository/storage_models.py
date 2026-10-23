from typing import Dict, Any, List, Optional
from datetime import datetime

class ObjectMetadata:
    def __init__(self, key: str, size_bytes: int, last_modified: datetime, etag: str, content_type: str):
        self.key = key
        self.size_bytes = size_bytes
        self.last_modified = last_modified
        self.etag = etag
        self.content_type = content_type

class PresignedUrlResult:
    def __init__(self, url: str):
        self.url = url

class UploadResult:
    def __init__(self, etag: str, version_id: Optional[str] = None):
        self.etag = etag
        self.version_id = version_id

class ListObjectsResult:
    def __init__(self, objects: List[ObjectMetadata], common_prefixes: List[str]):
        self.objects = objects
        self.common_prefixes = common_prefixes

def normalize_head_object_response(key: str, response: Dict[str, Any]) -> ObjectMetadata:
    return ObjectMetadata(
        key=key,
        size_bytes=response.get('ContentLength', 0),
        last_modified=response.get('LastModified', datetime.min),
        etag=response.get('ETag', '').strip('"'),
        content_type=response.get('ContentType', 'application/octet-stream')
    )

def normalize_list_objects_response(response: Dict[str, Any]) -> ListObjectsResult:
    objects = []
    if 'Contents' in response:
        for content in response['Contents']:
            objects.append(
                ObjectMetadata(
                    key=content.get('Key', ''),
                    size_bytes=content.get('Size', 0),
                    last_modified=content.get('LastModified', datetime.min),
                    etag=content.get('ETag', '').strip('"'),
                    content_type='application/octet-stream'
                )
            )
    common_prefixes = [p['Prefix'] for p in response.get('CommonPrefixes', [])]
    return ListObjectsResult(objects=objects, common_prefixes=common_prefixes)
