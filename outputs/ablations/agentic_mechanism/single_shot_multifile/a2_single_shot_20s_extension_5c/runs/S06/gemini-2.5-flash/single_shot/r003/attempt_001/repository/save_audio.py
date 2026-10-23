import os
import boto3

def save_audio_to_s3(audio_bytes: bytes, bucket_name: str, object_key: str) -> str:
    client = boto3.client(
        's3',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=audio_bytes,
        ContentType='audio/mpeg' 
    )
    return f"s3://{bucket_name}/{object_key}"

def save_audio_to_local_file(audio_bytes: bytes, file_path: str):
    with open(file_path, 'wb') as f:
        f.write(audio_bytes)
