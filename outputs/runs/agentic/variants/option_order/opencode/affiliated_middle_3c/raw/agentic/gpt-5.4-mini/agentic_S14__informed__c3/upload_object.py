import sys

import boto3

from storage_client import resolve_bucket
from storage_models import UploadObjectRequest, UploadObjectResponse


def upload_object(bucket: str, key: str, data, content_type: str | None = None):
    client = boto3.client("s3")
    request = UploadObjectRequest(
        bucket=resolve_bucket(bucket), key=key, content_type=content_type
    )
    kwargs = {"Bucket": request.bucket, "Key": request.key, "Body": data}
    if request.content_type:
        kwargs["ContentType"] = request.content_type
    result = client.put_object(**kwargs)
    return UploadObjectResponse(
        bucket=request.bucket,
        key=request.key,
        etag=result.get("ETag"),
        version_id=result.get("VersionId"),
    )


if __name__ == "__main__":
    bucket, key, path = sys.argv[1:4]
    with open(path, "rb") as f:
        print(upload_object(bucket, key, f.read()))
