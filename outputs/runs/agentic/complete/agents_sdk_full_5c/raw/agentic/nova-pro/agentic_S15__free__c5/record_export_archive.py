import boto3

def export_record(record, bucket_name, object_name):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=object_name, Body=record)
