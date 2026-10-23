import base64

from database_client import get_s3_client
from database_models import build_response


def record_export_archive(payload, config=None):
    client, cfg = get_s3_client(config)
    bucket = payload.get("bucket") or cfg["bucket_name"]
    key = payload.get("key") or f"exports/{payload['id']}.json"
    body = payload.get("content")
    if isinstance(body, str):
        data = body.encode("utf-8")
    elif isinstance(body, bytes):
        data = body
    else:
        data = base64.b64decode(payload.get("content_base64", ""))
    client.put_object(Bucket=bucket, Key=key, Body=data)
    return build_response({"bucket": bucket, "key": key})
