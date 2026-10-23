from storage_client import get_s3_client
from storage_models import UploadRequest, UploadResponse


def upload_object(request: UploadRequest) -> UploadResponse:
    client = get_s3_client()
    kwargs = {}
    if request.content_type:
        kwargs["ContentType"] = request.content_type
    if request.metadata:
        kwargs["Metadata"] = dict(request.metadata)
    result = client.put_object(Bucket=request.bucket, Key=request.key, Body=request.body, **kwargs)
    return UploadResponse(bucket=request.bucket, key=request.key, etag=result.get("ETag"), version_id=result.get("VersionId"))
