
import boto3

def get_object_metadata(bucket_name, object_key):
    """
    Reads object metadata (head information) from AWS S3.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The key (path) of the object in the bucket.

    Returns:
        dict: A dictionary containing the object's metadata, or None if an error occurs.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        # The 'ResponseMetadata' key is usually present and contains request details.
        # We are interested in the actual object metadata which is directly in the response.
        # For example, ContentType, LastModified, ContentLength, ETag, etc.
        # User-defined metadata will be under 'Metadata' key.
        return response
    except s3_client.exceptions.NoSuchKey:
        print(f"Object with key '{object_key}' not found in bucket '{bucket_name}'.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example Usage: Replace with your bucket name and object key
    # Ensure you have AWS credentials configured (e.g., via environment variables or ~/.aws/credentials)
    # Before running, make sure to install boto3: pip install boto3
    
    # bucket = "your-s3-bucket-name"
    # key = "path/to/your/object.txt"
    
    # metadata = get_object_metadata(bucket, key)
    
    # if metadata:
    #     print(f"Metadata for s3://{bucket}/{key}:")
    #     for k, v in metadata.items():
    #         print(f"  {k}: {v}")
    # else:
    #     print("Failed to retrieve object metadata.")
