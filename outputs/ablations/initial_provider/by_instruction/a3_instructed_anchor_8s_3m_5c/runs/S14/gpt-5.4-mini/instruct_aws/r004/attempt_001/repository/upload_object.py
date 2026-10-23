import boto3

from storage_client import get_bucket_name, get_s3_client, normalize_body
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(bucket=None, key=None, body=None, content_type=None, metadata=None):
    client = get_s3_client()
    req = UploadObjectRequest(bucket=bucket or get_bucket_name(), key=key, body=body, content_type=content_type, metadata=metadata)
    params = {"Bucket": req.bucket, "Key": req.key, "Body": normalize_body(req.body)}
    if req.content_type:
        params["ContentType"] = req.content_type
    if req.metadata:
        params["Metadata"] = {str(k): str(v) for k, v in req.metadata.items()}
    response = client.put_object(**params)
    return UploadObjectResponse(bucket=req.bucket, key=req.key, etag=response.get("ETag"), version_id=response.get("VersionId"))
