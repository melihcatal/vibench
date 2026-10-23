import boto3

# Initialize a session using Amazon S3
session = boto3.Session()
s3 = session.client(
    service_name='s3',
    region_name='us-west-2',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
)

# Request helper function
def request_object(bucket_name, object_key):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        return response
    except Exception as e:
        print(e)
        return None

# Response helper function
def response_object(response):
    if response is not None:
        return response['Body'].read()
    else:
        return None

# Normalization helper function
def normalize_object(data):
    # Implement your normalization logic here
    return data