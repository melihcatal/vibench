import boto3

def archive_image_assets(bucket_name, image_path, analysis_results):
    s3 = boto3.client('s3')
    s3.upload_file(image_path, bucket_name, 'image.jpg')
    s3.put_object(Bucket=bucket_name, Key='analysis_results.json', Body=analysis_results)