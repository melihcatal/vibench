import boto3
import os


def save_audio(payload, config=None):
    config = config or {}
    audio_bytes = payload['audio_bytes']
    file_path = payload['file_path']
    
    # Determine if saving to local file or S3
    if config.get('s3_bucket_name') and config.get('aws_access_key_id') and config.get('aws_secret_access_key'):
        s3 = boto3.client(
            's3',
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            region_name=config.get('aws_region', 'us-east-1')
        )
        bucket_name = config['s3_bucket_name']
        s3_key = os.path.basename(file_path) # Use the filename as the S3 key
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=audio_bytes)
        return {'status': 'success', 'location': f's3://{bucket_name}/{s3_key}'}
    else:
        # Save to local file
        with open(file_path, 'wb') as f:
            f.write(audio_bytes)
        return {'status': 'success', 'location': os.path.abspath(file_path)}