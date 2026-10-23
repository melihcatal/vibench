import boto3

def archive_image_analysis(bucket_name, key, analysis):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=key, Body=analysis)