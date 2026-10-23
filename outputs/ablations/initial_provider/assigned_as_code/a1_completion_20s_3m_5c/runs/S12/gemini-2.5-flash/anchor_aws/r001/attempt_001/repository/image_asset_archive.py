import json
from vision_client import VisionClient
from vision_models import ArchiveRequest, ArchiveResponse


def image_asset_archive(payload: ArchiveRequest, config=None) -> ArchiveResponse:
    config = config or {}
    region_name = config.get("region")
    client = VisionClient(region_name)

    client.s3_client.put_object(
        Bucket=payload.bucket_name,
        Key=payload.file_name,
        Body=payload.content,
        Metadata=payload.metadata if payload.metadata else {},
    )

    object_url = f"https://{payload.bucket_name}.s3.{region_name}.amazonaws.com/{payload.file_name}"
    return ArchiveResponse(object_url=object_url)