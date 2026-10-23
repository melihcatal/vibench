import boto3

def metrics_export_archive(metric_data, bucket_name):
    s3 = boto3.client('s3')
    s3.put_object(
        Body=metric_data,
        Bucket=bucket_name,
        Key='metrics/export.json'
    )