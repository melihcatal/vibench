import os
import boto3

def get_object_metadata(bucket_name: str, object_name: str):
    """
    Retrieves metadata for a specific object in an S3 bucket.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_name)
        # The 'ResponseMetadata' and 'ContentLength' etc. are part of the head_object response
        metadata = {
            "ContentLength": response.get('ContentLength'),
            "ContentType": response.get('ContentType'),
            "ETag": response.get('ETag'),
            "LastModified": response.get('LastModified'),
            "Metadata": response.get('Metadata', {})
        }
        return metadata
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"Object {object_name} not found in bucket {bucket_name}.")
        else:
            print(f"Error retrieving object metadata: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    # This is example usage and will not be run by the system.
    # Replace with actual values for testing
    # BUCKET = os.environ.get("S3_BUCKET_NAME", "your-s3-bucket-name")
    # KEY = "my-test-object.txt"
    # metadata = get_object_metadata(BUCKET, KEY)
    # if metadata:
    #     print(f"Object Metadata for {KEY}:")
    #     for k, v in metadata.items():
    #         print(f"  {k}: {v}")
    pass
