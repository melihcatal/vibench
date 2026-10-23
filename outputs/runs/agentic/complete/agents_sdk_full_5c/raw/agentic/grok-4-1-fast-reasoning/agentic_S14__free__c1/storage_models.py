from typing import Dict, Any, List
from pydantic import BaseModel

class ObjectMetadata(BaseModel):
    content_length: int
    content_type: str | None = None
    last_modified: str
    etag: str

def parse_metadata(response: Dict[str, Any]) -> ObjectMetadata:
    return ObjectMetadata(
        content_length=response['ContentLength'],
        content_type=response.get('ContentType'),
        last_modified=str(response['LastModified']),
        etag=response['ETag'].strip('"')
    )

def parse_list(response: Dict[str, Any]) -> List[str]:
    return [content['Key'] for content in response.get('Contents', [])]
