import boto3
from botocore.exceptions import NoCredentialsError

def create_presigned_download_url(bucket_name: str, object_name: str, expiration: int = 3600):
    """
    Generates a time-limited signed URL for downloading a stored object from AWS S3.

    :param bucket_name: Name of the S3 bucket.
    :param object_name: Name of the object in the S3 bucket.
    :param expiration: Time in seconds for the presigned URL to remain valid. Default is 1 hour (3600 seconds).
    :return: Presigned URL as a string.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
    except NoCredentialsError:
        print("AWS credentials not found. Please configure your AWS credentials.")
        return None
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None
    return response

