import boto3
from storage_client import get_s3_client

def list_objects_with_prefix(bucket_name, prefix=''):
    s3_client = get_s3_client()
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    except Exception as e:
        print(e)
        return None
    return response.get('Contents', [])

if __name__ == '__main__':
    print(list_objects_with_prefix('my-bucket', 'my-prefix/'))