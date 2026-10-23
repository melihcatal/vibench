import os
import json
from vision_client import get_s3_compatible_client
from vision_models import VisualAnalysis

def archive_analysis_to_r2(
    bucket_name: str,
    asset_id: str,
    image_bytes: bytes,
    analysis_data: VisualAnalysis,
) -> None:
    """
    Archives an image and its analysis results to Cloudflare R2.

    Args:
        bucket_name: The R2 bucket name.
        asset_id: A unique identifier for the image asset.
        image_bytes: The raw bytes of the image file.
        analysis_data: The Pydantic model containing the analysis results.
    """
    endpoint_url = os.environ.get("CLOUDFLARE_R2_ENDPOINT")
    access_key_id = os.environ.get("CLOUDFLARE_R2_ACCESS_KEY_ID")
    secret_access_key = os.environ.get("CLOUDFLARE_R2_SECRET_ACCESS_KEY")

    if not all([endpoint_url, access_key_id, secret_access_key]):
        raise ValueError("Cloudflare R2 environment variables are not properly set.")

    s3_client = get_s3_compatible_client(
        endpoint_url=endpoint_url,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
    )

    image_key = f"{asset_id}/original.jpg"
    analysis_key = f"{asset_id}/analysis.json"

    # Upload the original image
    s3_client.put_object(
        Bucket=bucket_name,
        Key=image_key,
        Body=image_bytes,
        ContentType='image/jpeg'
    )

    # Upload the analysis data as JSON
    analysis_json = analysis_data.model_dump_json(indent=2)
    s3_client.put_object(
        Bucket=bucket_name,
        Key=analysis_key,
        Body=analysis_json.encode('utf-8'),
        ContentType='application/json'
    )
