import boto3

def image_asset_archive(image_path, bucket_name):
    s3_client = boto3.client('s3')
    with open(image_path, 'rb') as image:
        s3_client.upload_fileobj(image, bucket_name, image_path.split('/')[-1])