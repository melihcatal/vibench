import boto3
from botocore.exceptions import ClientError

def create_presigned_download_url(bucket_name: str, object_name: str, expiration: int = 3600):
    """
    Generate a presigned URL to download an S3 object

    :param bucket_name: Name of the S3 bucket
    :param object_name: Key of the S3 object
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print(f"Error creating presigned URL: {e}")
        return None
    return response
