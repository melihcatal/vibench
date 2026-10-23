import boto3
from storage_client import get_s3_client

def create_presigned_url(bucket_name, object_key, expiration=3600):
    s3_client = get_s3_client()
    try:
        response = s3_client.generate_presigned_url('get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration)
    except Exception as e:
        print(e)
        return None
    return response

if __name__ == '__main__':
    print(create_presigned_url('my-bucket', 'my-object-key'))