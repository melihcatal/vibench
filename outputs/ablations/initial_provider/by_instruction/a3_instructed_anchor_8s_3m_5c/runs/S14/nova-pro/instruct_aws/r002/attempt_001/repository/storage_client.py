import boto3

def create_s3_client():
    return boto3.client('s3')

def get_bucket_region(bucket_name):
    s3_client = create_s3_client()
    response = s3_client.get_bucket_location(Bucket=bucket_name)
    return response['LocationConstraint']