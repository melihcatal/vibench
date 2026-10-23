from storage_client import get_s3_client


def get_object_metadata(bucket_name: str, object_key: str) -> dict:
    """
    Reads object metadata or head information from Amazon S3 managed object storage.
    """
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        # Extract relevant metadata, e.g., ContentLength, ContentType, LastModified, ETag
        metadata = {
            "ContentLength": response.get("ContentLength"),
            "ContentType": response.get("ContentType"),
            "LastModified": response.get("LastModified").isoformat()
            if response.get("LastModified")
            else None,
            "ETag": response.get("ETag"),
            "Metadata": response.get("Metadata", {}),
        }
        return {"status": "success", "metadata": metadata}
    except s3_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return {
                "status": "error",
                "message": f"Object {object_key} not found in {bucket_name}",
            }
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
