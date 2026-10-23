import boto3

def metrics_export_archive(metric_data, bucket_name):
    s3_client = boto3.client('s3')
    file_name = f"metrics_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    s3_client.put_object(Body=metric_data, Bucket=bucket_name, Key=file_name)