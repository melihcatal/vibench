import boto3

def get_object_metadata(bucket_name: str, object_key: str) -> dict:
    """
    Reads object metadata from an Amazon S3 bucket.

    Args:
        bucket_name: The name of the S3 bucket.
        object_key: The key of the object in the S3 bucket.

    Returns:
        A dictionary containing the object's metadata, or an empty dictionary if an error occurs.
    """
    s3_client = boto3.client("s3")
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        return response.get("Metadata", {})
    except s3_client.exceptions.ClientError as e:
        print(f"Error retrieving metadata for s3://{bucket_name}/{object_key}: {e}")
        return {}

