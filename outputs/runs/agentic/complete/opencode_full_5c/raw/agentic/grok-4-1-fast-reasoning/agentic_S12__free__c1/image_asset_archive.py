import boto3
import json
from dataclasses import asdict
from vision_models import FullVisionAnalysis


def image_asset_archive(
    image_path: str,
    analysis: FullVisionAnalysis,
    bucket_name: str,
    key_prefix: str = "analysis/",
):
    s3 = boto3.client("s3")
    # Upload image, assuming jpg
    image_key = f"{key_prefix}image.jpg"
    s3.upload_file(image_path, bucket_name, image_key)
    # Upload analysis JSON
    analysis_dict = asdict(analysis)
    analysis_key = f"{key_prefix}analysis.json"
    s3.put_object(
        Bucket=bucket_name, Key=analysis_key, Body=json.dumps(analysis_dict, indent=2)
    )
