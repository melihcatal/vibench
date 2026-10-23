from storage_client import get_storage_client
from botocore.exceptions import ClientError


def create_presigned_url(bucket_name: str, object_name: str, expiration: int = 3600):
    """
    Generate a presigned URL to share an S3 object.
    """
    s3_client = get_storage_client()
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        return {"error": str(e)}

    return {"url": response}
