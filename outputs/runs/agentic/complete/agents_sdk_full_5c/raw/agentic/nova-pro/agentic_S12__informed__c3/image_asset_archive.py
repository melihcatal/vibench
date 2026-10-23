import boto3

def archive_image(image_path, bucket_name):
    s3 = boto3.client('s3')
    with open(image_path, 'rb') as data:
        s3.upload_fileobj(data, bucket_name, image_path)
