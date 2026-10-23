import boto3
from storage_client import get_s3_client

def get_object_metadata(bucket_name, object_key):
    s3_client = get_s3_client()
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
    except Exception as e:
        print(e)
        return None
    return response

if __name__ == '__main__':
    print(get_object_metadata('my-bucket', 'my-object-key'))