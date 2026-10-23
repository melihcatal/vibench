import boto3

S3_BUCKET_NAME = 'your-s3-bucket-name'

def archive_image_analysis(image_path, analysis_results):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=S3_BUCKET_NAME, Key=image_path, Body=analysis_results)
    return f's3://{S3_BUCKET_NAME}/{image_path}'