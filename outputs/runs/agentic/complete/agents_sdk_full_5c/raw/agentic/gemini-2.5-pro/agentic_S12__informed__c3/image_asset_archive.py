
import os
import json
import boto3
from botocore.exceptions import ClientError

def archive_analysis(
    bucket_name: str,
    asset_id: str,
    image_path: str,
    analysis_results: dict
):
    """
    Archives image and its analysis results to Amazon S3.
    """
    s3_client = boto3.client("s3")

    # Upload the original image
    image_key = f"images/{asset_id}.jpg"
    try:
        s3_client.upload_file(image_path, bucket_name, image_key)
    except ClientError as e:
        print(f"Error uploading image to S3: {e}")
        raise

    # Upload the analysis results as a JSON file
    analysis_key = f"analysis/{asset_id}_analysis.json"
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=analysis_key,
            Body=json.dumps(analysis_results, indent=2),
            ContentType='application/json'
        )
    except ClientError as e:
        print(f"Error uploading analysis to S3: {e}")
        raise

    print(f"Successfully archived {asset_id} to bucket {bucket_name}")
