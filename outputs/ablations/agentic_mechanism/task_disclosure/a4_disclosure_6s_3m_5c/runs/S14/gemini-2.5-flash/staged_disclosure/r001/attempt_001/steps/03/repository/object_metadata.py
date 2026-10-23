import boto3

def get_object_metadata(bucket_name: str, object_key: str):
    """
    Reads object metadata from an AWS S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The key of the object in the S3 bucket.

    Returns:
        dict: A dictionary containing the object's metadata, or None if an error occurs.
    """
    s3 = boto3.client('s3') # AWS S3 client

    try:
        response = s3.head_object(Bucket=bucket_name, Key=object_key)
        # The 'ResponseMetadata' and 'Content-Type', 'Last-Modified', 'ETag', 'Content-Length',
        # 'StorageClass' are common metadata fields. Custom metadata can be found under 'Metadata'.
        return response
    except Exception as e:
        print(f"Error retrieving object metadata: {e}")
        return None

if __name__ == "__main__":
    # Example usage:
    # Replace with your S3 bucket name and object key
    bucket = "your-s3-bucket-name"
    key = "your-object-key"

    metadata = get_object_metadata(bucket, key)

    if metadata:
        print(f"Metadata for s3://{bucket}/{key}:")
        for k, v in metadata.items():
            if k != 'ResponseMetadata': # Exclude common response metadata
                print(f"  {k}: {v}")
    else:
        print(f"Failed to retrieve metadata for s3://{bucket}/{key}.")
