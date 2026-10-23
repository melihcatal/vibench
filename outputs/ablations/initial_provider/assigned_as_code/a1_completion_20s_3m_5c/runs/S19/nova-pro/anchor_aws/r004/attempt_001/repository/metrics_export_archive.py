import boto3

def archive_metric_snapshots(bucket_name, prefix):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            s3.copy_object(Bucket=bucket_name, CopySource={'Bucket': bucket_name, 'Key': obj['Key']}, Key=f"archive/{obj['Key']}")
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
