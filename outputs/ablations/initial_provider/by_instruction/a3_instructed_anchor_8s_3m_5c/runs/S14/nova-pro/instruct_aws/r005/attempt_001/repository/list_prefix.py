import boto3

def list_objects(bucket_name, prefix=''):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    except ClientError as e:
        logging.error(e)
        return None
    return response