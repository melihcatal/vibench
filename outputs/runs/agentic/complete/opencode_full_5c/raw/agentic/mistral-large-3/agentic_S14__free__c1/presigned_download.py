import os
from storage_client import StorageClient
from storage_models import PresignedDownloadRequest, PresignedDownloadResponse


def presigned_download(
    bucket_name: str, object_key: str, expires_in: int = 3600
) -> PresignedDownloadResponse:
    """
    Creates a time-limited signed download URL for an object stored in Amazon S3.
    """
    client = StorageClient().get_client()

    request: PresignedDownloadRequest = {
        "bucket_name": bucket_name,
        "object_key": object_key,
        "expires_in": expires_in,
    }

    try:
        url = client.generate_presigned_url(
            "get_object",
            Params={"Bucket": request["bucket_name"], "Key": request["object_key"]},
            ExpiresIn=request["expires_in"],
        )
        return {"url": url}
    except Exception as e:
        raise Exception(f"Failed to generate presigned URL for S3 object: {str(e)}")
