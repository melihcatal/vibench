from storage_client import get_bucket_name, get_s3_client
from storage_models import PresignedDownloadRequest


def create_presigned_download_url(bucket=None, key=None, expires_in=3600):
    client = get_s3_client()
    req = PresignedDownloadRequest(bucket=bucket or get_bucket_name(), key=key, expires_in=expires_in)
    return client.generate_presigned_url("get_object", Params={"Bucket": req.bucket, "Key": req.key}, ExpiresIn=req.expires_in)
