import boto3

def archive_image_analysis(image_path, analysis_results):
    s3 = boto3.client('s3')
    bucket_name = os.getenv('S3_BUCKET_NAME')
    s3.put_object(Bucket=bucket_name, Key=image_path, Body=analysis_results)