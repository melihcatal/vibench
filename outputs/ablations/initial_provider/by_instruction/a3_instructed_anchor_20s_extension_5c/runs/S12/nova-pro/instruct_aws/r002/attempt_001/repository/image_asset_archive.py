import boto3

def archive_image_analysis(image_path, analysis_results):
    s3_client = boto3.client('s3')
    bucket_name = 'image-analysis-archive'
    key = f'{image_path.split('/')[-1]}.json'
    s3_client.put_object(
        Body=json.dumps(analysis_results),
        Bucket=bucket_name,
        Key=key
    )