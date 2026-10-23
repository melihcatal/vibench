import boto3

from storage_client import get_s3_client


def create_presigned_download(object_name, bucket, config=None):
    config = config or {}
    client = get_s3_client(config)
    response = client.generate_presigned_url('get_object',
                                             Params={'Bucket': bucket, 'Key': object_name},
                                             ExpiresIn=3600)
    return response