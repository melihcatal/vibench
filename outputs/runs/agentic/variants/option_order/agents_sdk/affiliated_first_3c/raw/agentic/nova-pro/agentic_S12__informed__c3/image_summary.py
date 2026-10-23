import boto3

s3 = boto3.client('s3')

def summarize_image(bucket_name, object_key):
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    summary = response['Body'].read()
    print('Summary:', summary)