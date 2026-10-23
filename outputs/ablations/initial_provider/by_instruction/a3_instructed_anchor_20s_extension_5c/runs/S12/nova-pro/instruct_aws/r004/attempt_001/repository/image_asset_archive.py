import boto3

def archive_image_analysis(image_path, analysis_results):
    s3_client = boto3.client('s3')
    s3_client.put_object(
        Body=analysis_results,
        Bucket='image-analysis-archive',
        Key=f'{image_path}-analysis.json'
    )