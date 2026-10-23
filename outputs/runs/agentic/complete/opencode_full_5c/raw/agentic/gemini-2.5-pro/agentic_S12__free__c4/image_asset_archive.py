import os
import json
import boto3
from urllib.parse import urlparse
from vision_models import ArchiveRequest


def archive_assets(request: ArchiveRequest):
    """Archives image-analysis artifacts and captions to S3."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION"),
    )

    bucket_name = os.environ.get("S3_BUCKET_NAME")
    parsed_url = urlparse(request.image_uri)
    image_filename = os.path.basename(parsed_url.path)
    base_filename = os.path.splitext(image_filename)[0]

    # Archive analysis results
    analysis_filename = f"{base_filename}_analysis.json"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=f"analysis/{analysis_filename}",
        Body=json.dumps(request.analysis_results),
        ContentType="application/json",
    )

    # Archive caption
    caption_filename = f"{base_filename}_caption.txt"
    s3_client.put_object(
        Bucket=bucket_name,
        Key=f"captions/{caption_filename}",
        Body=request.caption,
        ContentType="text/plain",
    )

    # Archive original image (by copying from source URI if it's also on S3, or downloading and re-uploading)
    # This is a simplified example assuming the file is accessible.
    if parsed_url.scheme == "s3":
        copy_source = {"Bucket": parsed_url.netloc, "Key": parsed_url.path.lstrip("/")}
        s3_client.copy_object(
            Bucket=bucket_name, Key=f"images/{image_filename}", CopySource=copy_source
        )
    else:
        # For non-S3 URIs, you would download the image first.
        # import requests
        # response = requests.get(request.image_uri)
        # s3_client.put_object(Bucket=bucket_name, Key=f"images/{image_filename}", Body=response.content)
        pass  # Placeholder for non-S3 URIs

    return {
        "analysis_archive_path": f"s3://{bucket_name}/analysis/{analysis_filename}",
        "caption_archive_path": f"s3://{bucket_name}/captions/{caption_filename}",
        "image_archive_path": f"s3://{bucket_name}/images/{image_filename}",
    }
