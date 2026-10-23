from storage_client import get_s3_client


def create_presigned_download_url(
    bucket_name: str,
    object_key: str,
    expiration: int = 3600,  # URL expiration in seconds
) -> dict:
    """
    Creates a time-limited signed download URL for a stored object in Amazon S3.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
        return {"status": "success", "url": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}
