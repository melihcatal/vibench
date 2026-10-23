import boto3

from storage_client import get_s3_client


def create_presigned_download(object_name, expiration=3600):
    client = get_s3_client()
    response = client.generate_presigned_url('get_object',
                                            Params={'Bucket': 'your-bucket-name', 'Key': object_name},
                                            ExpiresIn=expiration)
    return response