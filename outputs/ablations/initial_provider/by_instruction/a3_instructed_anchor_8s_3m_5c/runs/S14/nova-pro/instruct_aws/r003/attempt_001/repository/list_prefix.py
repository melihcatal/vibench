import boto3

def list_prefix(bucket_name, prefix=''):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    return response.get('Contents', [])