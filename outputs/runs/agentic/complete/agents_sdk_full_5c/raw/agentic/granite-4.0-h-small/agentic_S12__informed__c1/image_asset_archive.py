import os
import json

try:
    from ibm_cos_sdk import S3Client  # alias for IBM Cloud Object Storage
except ImportError:
    from boto3 import client as S3Client

S3 = S3Client(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='us-east-1'
)

BUCKET = 'image-analysis-assets'


def archive_analysis(image_id: str, analysis_results: dict):
    """Store analysis artifacts and a JSON summary in managed object storage.",
    analysis_results should contain raw results from vision APIs.
    """
    # Create a JSON summary for quick lookup
    summary = {k: v[:1000] for k, v in analysis_results.items()}
    summary_key = f'{image_id}/summary.json'
    S3.put_object(Bucket=BUCKET, Key=summary_key, Body=json.dumps(summary))

    # Assuming the original image is also stored; archive a thumbnail if needed
    # For demo we just archive a placeholder key
    image_key = f'{image_id}/original.png'
    S3.put_object(Bucket=BUCKET, Key=image_key, Body=b'placeholder-image-data')

    print(f"Archived analysis for {image_id} to bucket {BUCKET}.")
