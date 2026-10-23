from io import BytesIO
from typing import Any, Dict
import json

from database_client import get_bucket_name, get_s3_client


def export_archive(snapshot: Dict[str, Any], key_prefix: str = "exports/") -> Dict[str, Any]:
    s3 = get_s3_client()
    bucket = get_bucket_name()
    key = f"{key_prefix.rstrip('/')}/{snapshot.get('document_id', 'unknown')}.json"
    body = BytesIO(json.dumps(snapshot, ensure_ascii=False, default=str).encode("utf-8"))
    s3.upload_fileobj(body, bucket, key, ExtraArgs={"ContentType": "application/json"})
    return {"bucket": bucket, "key": key, "archived": True}
