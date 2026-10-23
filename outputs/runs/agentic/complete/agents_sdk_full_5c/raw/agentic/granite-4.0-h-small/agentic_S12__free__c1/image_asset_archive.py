import json, boto3, os

def archive_analysis(analysis_id: str, analysis_data: dict, bucket_name: str, prefix: str = ''):
    """Upload analysis results to Amazon S3 as JSON.",
    # Ensure analysis_id is safe for S3 key naming
    key = f'{prefix}{analysis_id}.json'
    s3 = boto3.client('s3')
    # Simple retry loop for robustness
    for attempt in range(3):
        try:
            s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(analysis_data).encode('utf-8'))
            print(f'Archived {key} to s3://{bucket_name}')
            return True
        except Exception as e:
            print(f'Attempt {attempt+1} failed: {e}')
    print('Archive failed after retries')
    return False
