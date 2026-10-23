import os
import boto3

def create_presigned_download_url(bucket_name: str, object_name: str, expiration: int = 3600):
    """
    Generate a presigned URL to share an S3 object.
    :param bucket_name: String name of the S3 bucket.
    :param object_name: String name of the S3 object.
    :param expiration: Time in seconds for the presigned URL to remain valid.
    :return: Presigned URL as string.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
        return response
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None

if __name__ == '__main__':
    # This is example usage and will not be run by the system.
    # Replace with actual values for testing
    # BUCKET = os.environ.get("S3_BUCKET_NAME", "your-s3-bucket-name")
    # KEY = "my-test-object.txt"
    # url = create_presigned_download_url(BUCKET, KEY)
    # if url:
    #     print(f"Presigned URL: {url}")
    pass
