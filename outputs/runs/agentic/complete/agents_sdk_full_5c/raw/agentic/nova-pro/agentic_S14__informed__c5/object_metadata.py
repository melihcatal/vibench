import boto3

def get_object_metadata(bucket_name, object_name):
    s3_client = boto3.client('s3')
    response = s3_client.head_object(Bucket=bucket_name, Key=object_name)
    return response