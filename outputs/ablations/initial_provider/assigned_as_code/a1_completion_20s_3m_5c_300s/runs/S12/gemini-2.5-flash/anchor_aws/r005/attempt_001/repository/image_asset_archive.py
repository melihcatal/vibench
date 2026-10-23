import json
from vision_client import get_s3_client


def image_asset_archive(payload, config=None):
    config = config or {}
    client = get_s3_client(region_name=config.get("region"))

    bucket_name = config.get("bucket_name")
    object_key_prefix = config.get("object_key_prefix", "image_analysis/")
    image_id = payload.get("image_id", "default_image")

    if not bucket_name:
        return {"status": "error", "message": "S3 bucket_name not provided in config."}

    # Archive image bytes (if available)
    if "image_bytes" in payload:
        image_key = f"{object_key_prefix}{image_id}.jpg"  # Assuming JPEG for example
        client.put_object(
            Bucket=bucket_name,
            Key=image_key,
            Body=payload["image_bytes"],
            ContentType="image/jpeg"
        )
        print(f"Archived image to s3://{bucket_name}/{image_key}")

    # Archive analysis results (as JSON)
    analysis_results = {
        k: v for k, v in payload.items() if k not in ["image_bytes"]
    } # Exclude raw image bytes from JSON artifact
    if analysis_results:
        analysis_key = f"{object_key_prefix}{image_id}_analysis.json"
        client.put_object(
            Bucket=bucket_name,
            Key=analysis_key,
            Body=json.dumps(analysis_results),
            ContentType="application/json"
        )
        print(f"Archived analysis results to s3://{bucket_name}/{analysis_key}")

    return {"status": "success", "message": "Image assets and analysis archived."}
