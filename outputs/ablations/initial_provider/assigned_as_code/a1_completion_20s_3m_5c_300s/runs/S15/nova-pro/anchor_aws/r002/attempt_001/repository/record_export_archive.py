import boto3


def record_export_archive(document, bucket_name, key, config):
    s3 = boto3.client('s3', region_name=config['region'])
    s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(document))