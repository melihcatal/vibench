import boto3

def archive_image_analysis(bucket_name, image_path, analysis_results):
    s3_client = boto3.client('s3')
    with open(image_path, 'rb') as image:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f'{image_path.split('/')[-1]}.analysis',
            Body=analysis_results
        )