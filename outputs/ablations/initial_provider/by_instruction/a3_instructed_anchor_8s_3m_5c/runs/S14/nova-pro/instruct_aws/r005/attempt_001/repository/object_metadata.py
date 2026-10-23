import boto3

def get_object_metadata(bucket_name, object_key):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
    except ClientError as e:
        logging.error(e)
        return None
    return response