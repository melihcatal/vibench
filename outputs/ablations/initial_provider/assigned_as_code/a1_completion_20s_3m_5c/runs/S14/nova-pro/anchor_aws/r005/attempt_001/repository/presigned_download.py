import boto3

from storage_client import get_s3_client


def create_presigned_download(object_name, expiration=3600):
    s3_client = get_s3_client()
    response = s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': 'your-bucket-name', 'Key': object_name},
                                                ExpiresIn=expiration)
    return response