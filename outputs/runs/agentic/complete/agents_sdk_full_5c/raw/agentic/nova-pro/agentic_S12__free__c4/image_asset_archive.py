import boto3

def archive_image(image_path, bucket_name, object_name):
    s3 = boto3.client('s3')
    s3.upload_file(image_path, bucket_name, object_name)