from storage_client import get_storage_client


def create_presigned_download_url(
    bucket: str, key: str, expiration_seconds: int = 3600
) -> str:
    s3_client = get_storage_client()
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expiration_seconds,
        )
        return response
    except Exception as e:
        print(f"Error creating presigned URL: {e}")
        return ""
