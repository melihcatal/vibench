from typing import TypedDict, List, Dict, Any, Optional

class S3ObjectSummary(TypedDict):
    key: str
    size: int
    last_modified: str
    etag: str
    storage_class: Optional[str]

class HeadObjectMetadata(TypedDict):
    content_length: int
    content_type: Optional[str]
    content_encoding: Optional[str]
    last_modified: str
    etag: str
    metadata: Dict[str, str]

def normalize_object_summary(raw_obj: Dict[str, Any]) -> S3ObjectSummary:
    return {
        'key': raw_obj['Key'],
        'size': raw_obj['Size'],
        'last_modified': raw_obj['LastModified'].isoformat() if raw_obj['LastModified'] else '',
        'etag': raw_obj['ETag'],
        'storage_class': raw_obj.get('StorageClass')
    }

def normalize_head_metadata(raw_meta: Dict[str, Any]) -> HeadObjectMetadata:
    return {
        'content_length': raw_meta['ContentLength'],
        'content_type': raw_meta.get('ContentType'),
        'content_encoding': raw_meta.get('ContentEncoding'),
        'last_modified': raw_meta['LastModified'].isoformat() if raw_meta['LastModified'] else '',
        'etag': raw_meta['ETag'],
        'metadata': dict(raw_meta.get('Metadata', {}))
    }
