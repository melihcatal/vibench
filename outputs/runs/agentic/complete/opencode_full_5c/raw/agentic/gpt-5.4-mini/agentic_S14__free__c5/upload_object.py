import base64

from storage_client import bucket_name, client
from storage_models import normalize_metadata


def upload_object(
    bucket: str | None,
    key: str,
    body,
    content_type: str | None = None,
    metadata: dict | None = None,
):
    s3 = client()
    data = body
    if isinstance(body, str) and body.startswith("base64:"):
        data = base64.b64decode(body.split(":", 1)[1])
    kwargs = {"Bucket": bucket_name(bucket), "Key": key, "Body": data}
    if content_type:
        kwargs["ContentType"] = content_type
    meta = normalize_metadata(metadata)
    if meta:
        kwargs["Metadata"] = meta
    return s3.put_object(**kwargs)
