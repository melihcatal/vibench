import json
import os
import boto3
from vision_client import VisionClient


def archive_artifacts(
    image_path: str, summary: dict, bucket_name: str, prefix: str = "image-analysis/"
):
    """Archives image analysis artifacts (image file, summary JSON) to Amazon S3.

    Requires AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.
    """
    client = VisionClient()  # reuses AWS configuration
    # Read the original image bytes
    original_bytes = client.read_image(image_path)
    # Prepare summary JSON string
    summary_json = json.dumps(summary, indent=2)
    s3 = boto3.resource("s3")
    # Upload image
    s3.Bucket(bucket_name).put_object(
        Key=prefix + os.path.basename(image_path), Body=original_bytes
    )
    # Upload summary
    s3.Bucket(bucket_name).put_object(
        Key=prefix + os.path.basename(image_path).rsplit(".", 1)[0] + ".json",
        Body=summary_json.encode(),
    )
