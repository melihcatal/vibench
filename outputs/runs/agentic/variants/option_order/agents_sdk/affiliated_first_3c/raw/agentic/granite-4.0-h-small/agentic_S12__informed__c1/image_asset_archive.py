import os
import json
import boto3

S3_BUCKET = os.getenv('S3_BUCKET')  # managed object storage bucket name
POSTFIX = 'image_analysis/'

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def _upload_to_s3(key: str, content: str):
    s3_client.put_object(Bucket=S3_BUCKET, Key=key, Body=content)

def archive_analysis(image_path: str, labels: list, description: str, translation: str, safe: bool):
    """Archive analysis artifacts in S3 as a JSON manifest file.\n    Files uploaded: manifest.json and the original image.
    """
    manifest = {
        'image_path': image_path,
        'labels': labels,
        'description': description,
        'translated_description': translation,
        'safety_status': safe
    }
    manifest_key = f"{POSTFIX}{os.path.basename(image_path.split('.')[0])}_analysis.json"
    _upload_to_s3(manifest_key, json.dumps(manifest, indent=2))
    # Upload the original image alongside the manifest
    _upload_to_s3(f"{POSTFIX}{os.path.basename(image_path)}", open(image_path, 'rb').read())
