import boto3

def get_object_metadata(bucket_name, object_key):
    """
    Reads object metadata from AWS S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The key of the object in the S3 bucket.

    Returns:
        dict: A dictionary containing the object metadata, or None if an error occurs.
    """
    s3 = boto3.client('s3')
    try:
        response = s3.head_object(Bucket=bucket_name, Key=object_key)
        return response['Metadata']
    except Exception as e:
        print(f"Error retrieving object metadata: {e}")
        return None

if __name__ == '__main__':
    # Example usage (replace with your bucket and object details)
    bucket = 'your-s3-bucket-name'
    key = 'your-object-key'
    metadata = get_object_metadata(bucket, key)
    if metadata:
        print(f"Metadata for s3://{bucket}/{key}:")
        for k, v in metadata.items():
            print(f"  {k}: {v}")
    else:
        print(f"Failed to retrieve metadata for s3://{bucket}/{key}")
