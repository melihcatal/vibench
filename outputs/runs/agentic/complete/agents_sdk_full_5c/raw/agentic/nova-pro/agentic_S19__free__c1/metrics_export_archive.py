import boto3

def export_metrics(bucket_name, object_key):
    s3 = boto3.client('s3')
    s3.upload_file('metrics.csv', bucket_name, object_key)