import boto3

s3 = boto3.client('s3')

def object_metadata(bucket_name, object_name):
    response = s3.head_object(Bucket=bucket_name, Key=object_name)
    return response