import os
import datetime
from storage_client import get_managed_storage_client


def presigned_download_url(bucket_name, object_key, expires_seconds=3600):
    """Create a time-limited signed download URL.

    Uses ibm-cos-sdk to generate a presigned URL for IBM Cloud Object Storage.
    """
    cos = get_managed_storage_client()
    expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_seconds)
    url = cos.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_key},
        ExpiresIn=int(expires_seconds),
    )
    return url
