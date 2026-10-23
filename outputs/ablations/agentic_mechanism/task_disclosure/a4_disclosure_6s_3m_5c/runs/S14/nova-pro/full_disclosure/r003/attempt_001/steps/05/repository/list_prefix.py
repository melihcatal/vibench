import boto3

def list_prefix(bucket_name, prefix):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        return [obj['Key'] for obj in response['Contents']]
    else:
        return []