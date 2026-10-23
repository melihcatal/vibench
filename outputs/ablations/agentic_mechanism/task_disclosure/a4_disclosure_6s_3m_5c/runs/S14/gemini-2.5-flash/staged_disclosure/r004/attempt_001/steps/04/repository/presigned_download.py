import boto3
from botocore.exceptions import ClientError

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: String
    :param object_name: String
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print(f"Error creating presigned URL: {e}")
        return None

    # The response contains the presigned URL
    return response

if __name__ == '__main__':
    # Example usage (replace with your actual bucket and object details)
    # Ensure you have AWS credentials configured (e.g., via environment variables or ~/.aws/credentials)
    bucket = 'your-s3-bucket-name'
    key = 'your-object-key'
    
    # You can specify a different expiration time if needed (e.g., 600 seconds = 10 minutes)
    url = create_presigned_url(bucket, key)

    if url:
        print(f"Presigned URL for '{key}' in bucket '{bucket}':\n{url}")
    else:
        print("Could not generate presigned URL.")
