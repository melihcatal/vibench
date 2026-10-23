import boto3
from botocore.exceptions import NoCredentialsError

def get_presigned_url(bucket_name, object_key, expiration=3600):
    try:
        s3_client = boto3.client('s3')
        response = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_key}, ExpiresIn=expiration)
        return response
    except NoCredentialsError:
        return 'Credentials not available'