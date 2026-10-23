from typing import TypedDict, List, Dict, Any, Optional
import datetime

class S3Object(TypedDict):
    key: str
    size: int
    last_modified: str
    etag: Optional[str]

def normalize_s3_object(raw_obj: Dict[str, Any]) -> S3Object:
    """Normalize S3 object info."""
    last_mod = raw_obj['LastModified']
    if hasattr(last_mod, 'isoformat'):
        last_mod_str = last_mod.isoformat()
    else:
        last_mod_str = str(last_mod)
    return {
        'key': raw_obj['Key'],
        'size': raw_obj['Size'],
        'last_modified': last_mod_str,
        'etag': raw_obj.get('ETag')
    }