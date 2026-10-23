import os
from storage_client import get_s3_client


def get_object_metadata(payload, config=None):
    config = config or {}
    bucket_name = config.get("bucket", os.environ.get("AWS_S3_BUCKET_NAME"))
    object_name = payload["object_name"]

    s3_client = get_s3_client(config.get("region"))

    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_name)
        # Extract relevant metadata, typically from the 'ResponseMetadata' and custom 'Metadata' fields
        metadata = {
            "content_type": response.get("ContentType"),
            "content_length": response.get("ContentLength"),
            "last_modified": response.get("LastModified").isoformat() if response.get("LastModified") else None,
            "etag": response.get("ETag"),
            "user_metadata": response.get("Metadata", {})
        }
        return metadata
    except s3_client.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise FileNotFoundError(f"Object {object_name} not found in bucket {bucket_name}")
        else:
            raise RuntimeError(f"Error retrieving object metadata: {e}")
