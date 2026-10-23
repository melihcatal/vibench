import boto3

def get_object_metadata(bucket_name: str, object_key: str) -> dict:
    """
    Reads object metadata from an S3 bucket.

    Args:
        bucket_name: The name of the S3 bucket.
        object_key: The key of the object to retrieve metadata for.

    Returns:
        A dictionary containing the object's metadata and head information.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        return response
    except s3_client.exceptions.ClientError as e:
        print(f"Error retrieving object metadata: {e}")
        return {}

