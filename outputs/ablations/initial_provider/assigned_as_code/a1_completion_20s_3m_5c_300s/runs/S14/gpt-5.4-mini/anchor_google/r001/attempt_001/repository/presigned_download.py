from datetime import timedelta

from storage_client import get_blob
from storage_models import normalize_object_name


def presigned_download(payload, config=None):
    blob, _ = get_blob(normalize_object_name(payload), config)
    expires_in = int(payload.get("expires_in", 3600))
    url = blob.generate_signed_url(version="v4", expiration=timedelta(seconds=expires_in), method="GET")
    return {"url": url, "expires_in": expires_in, "object_name": payload["object_name"]}
