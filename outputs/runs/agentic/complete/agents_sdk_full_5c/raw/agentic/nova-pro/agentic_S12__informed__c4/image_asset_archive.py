import boto3

def archive_image_asset(image_path, bucket_name, object_name):
    s3_client = boto3.client('s3')
    with open(image_path, 'rb') as data:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=data)