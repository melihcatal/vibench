from boto3 import client

class S3Request:
    def __init__(self, bucket_name, key):
        self.bucket_name = bucket_name
        self.key = key

class S3Response:
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body

def normalize_s3_response(response):
    return S3Response(response['ResponseMetadata']['HTTPStatusCode'], response['Body'].read())

s3_client = client('s3')