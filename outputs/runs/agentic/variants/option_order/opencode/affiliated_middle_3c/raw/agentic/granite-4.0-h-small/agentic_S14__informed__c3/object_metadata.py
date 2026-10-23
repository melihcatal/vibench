import boto3


def get_object_metadata(bucket_name, object_key):
    """Retrieve metadata (HEAD) for an object stored in Amazon S3.

    Uses the boto3 SDK – the provider is identified by boto3 import and
    AWS_* environment variables.
    """
    s3 = boto3.client("s3")
    try:
        response = s3.head_object(Bucket=bucket_name, Key=object_key)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch metadata: {e}")
    return response

    print(f"Metadata retrieved for {object_key} in bucket {bucket_name}")
