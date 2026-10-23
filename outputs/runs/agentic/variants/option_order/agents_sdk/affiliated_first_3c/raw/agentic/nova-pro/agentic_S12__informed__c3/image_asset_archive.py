import boto3

s3 = boto3.client('s3')

def archive_image(bucket_name, object_key, file_path):
    s3.upload_file(file_path, bucket_name, object_key)
    print('Image archived successfully.')