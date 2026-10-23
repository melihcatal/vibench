import boto3

s3 = boto3.client('s3')

def list_prefix(bucket_name, prefix=''):
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    return response.get('Contents', [])