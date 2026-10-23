import boto3

def list_prefix(bucket_name, prefix):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print('No objects found with the given prefix.')

# Example usage:
# list_prefix('my-bucket', 'my-prefix')