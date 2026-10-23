import boto3

def summarize_stored_asset(bucket_name, asset_key):
    comprehend_client = boto3.client('comprehend')
    s3_client = boto3.client('s3')
    asset_obj = s3_client.get_object(Bucket=bucket_name, Key=asset_key)
    asset_text = asset_obj['Body'].read().decode('utf-8')
    response = comprehend_client.start_dominant_language_detection_job(Text=asset_text)
    job_id = response['JobId']
    while True:
        response = comprehend_client.describe_dominant_language_detection_job(JobId=job_id)
        if response['DominantLanguageDetectionJobProperties']['JobStatus'] == 'COMPLETED':
            break
    return response