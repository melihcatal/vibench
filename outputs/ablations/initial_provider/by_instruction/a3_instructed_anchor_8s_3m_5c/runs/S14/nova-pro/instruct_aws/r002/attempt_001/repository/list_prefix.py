import boto3

def list_objects(bucket_name, prefix=''):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(f'Object: {obj['Key']}')
    else:
        print('No objects found.')