import json
from vision_client import get_s3_client
from vision_models import VisionAnalysis


def archive_analysis(
    bucket_name: str,
    object_name: str,
    analysis: VisionAnalysis,
    translated_text: str,
    summary: str,
):
    s3_client = get_s3_client()

    archive_data = {
        "analysis": analysis.model_dump(),
        "translated_alt_text": translated_text,
        "summary": summary,
    }

    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=json.dumps(archive_data, indent=2),
        ContentType="application/json",
    )
