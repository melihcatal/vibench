import boto3

def archive_image_analysis_artifacts(bucket_name, artifacts):
    s3 = boto3.client('s3')
    for key, value in artifacts.items():
        s3.put_object(Bucket=bucket_name, Key=key, Body=value)