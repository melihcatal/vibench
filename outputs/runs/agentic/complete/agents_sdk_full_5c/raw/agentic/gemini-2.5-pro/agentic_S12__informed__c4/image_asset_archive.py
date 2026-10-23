import os
import json
import boto3
from botocore.exceptions import ClientError

def archive_results(
    image_id: str, analysis_summary: str, translated_alt_text: str
) -> bool:
    """
    Archives image analysis results to an Amazon S3 bucket.

    Args:
        image_id: A unique identifier for the image.
        analysis_summary: The summary text of the analysis.
        translated_alt_text: The translated alt text.

    Returns:
        True if the file was uploaded successfully, False otherwise.
    """
    bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("AWS_S3_BUCKET_NAME environment variable not set.")
    
    s3_client = boto3.client("s3")
    
    archive_data = {
        "imageId": image_id,
        "summary": analysis_summary,
        "translatedAltText": translated_alt_text,
    }
    
    file_content = json.dumps(archive_data, indent=2)
    object_key = f"analysis-results/{image_id}.json"

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=file_content,
            ContentType="application/json"
        )
        print(f"Successfully uploaded {object_key} to {bucket_name}")
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return False
    
    return True
