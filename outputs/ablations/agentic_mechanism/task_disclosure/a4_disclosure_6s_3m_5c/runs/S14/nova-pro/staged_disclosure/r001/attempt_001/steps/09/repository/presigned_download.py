import boto3
from botocore.exceptions import NoCredentialsError

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    try:
        s3_client = boto3.client('s3')
        response = s3_client.generate_presigned_url('get_object',
                                                     Params={'Bucket': bucket_name,
                                                             'Key': object_name},
                                                     ExpiresIn=expiration)
        return response
    except NoCredentialsError:
        return 'Credentials not available'

# Example usage:
# url = generate_presigned_url('mybucket', 'myobject')
# print(url)