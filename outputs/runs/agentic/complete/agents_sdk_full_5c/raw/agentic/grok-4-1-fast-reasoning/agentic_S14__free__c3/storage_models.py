from dataclasses import dataclass
from typing import List

@dataclass
class ObjectInfo:
    key: str
    size: int
    last_modified: str
    etag: str

def normalize_object_list(contents: List[dict]) -> List[ObjectInfo]:
    return [
        ObjectInfo(
            key=obj['Key'],
            size=obj.get('Size', 0),
            last_modified=obj['LastModified'].isoformat() if 'LastModified' in obj else '',
            etag=obj.get('ETag', '')
        )
        for obj in contents
    ]