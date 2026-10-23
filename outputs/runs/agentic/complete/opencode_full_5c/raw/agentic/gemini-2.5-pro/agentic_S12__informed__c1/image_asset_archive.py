import boto3
import json
from dataclasses import asdict
from vision_models import VisionAnalysisResult


def image_asset_archive(
    bucket_name: str, asset_id: str, analysis_result: VisionAnalysisResult
):
    """
    Archives the image analysis artifacts to an Amazon S3 bucket.
    """
    s3_client = boto3.client(
        "s3",
        # AWS credentials will be sourced from environment variables
        # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
    )

    analysis_data = asdict(analysis_result)
    analysis_json = json.dumps(analysis_data, indent=2)

    object_key = f"analysis/{asset_id}.json"

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=analysis_json,
            ContentType="application/json",
        )
        print(
            f"Successfully archived analysis for {asset_id} to s3://{bucket_name}/{object_key}"
        )
        return True
    except Exception as e:
        print(f"Failed to archive analysis for {asset_id}: {e}")
        return False
