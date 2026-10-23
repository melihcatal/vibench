import boto3


def metrics_export_archive(metric_data, bucket_name):
    s3 = boto3.client('s3')
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    key = f'metrics/{timestamp}.json'
    s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(metric_data))