import boto3

def metrics_export_archive(bucket_name, file_name):
    s3 = boto3.client('s3')
    response = s3.upload_file('/tmp/' + file_name, bucket_name, file_name)
    return response