from vision_client import VisionClient
from vision_models import ImageAssetArchiveRequest, ImageAssetArchiveResponse
import os

def image_asset_archive(request: ImageAssetArchiveRequest) -> ImageAssetArchiveResponse:
    client = VisionClient(region_name=os.environ.get('AWS_REGION', 'us-east-1')).s3_client
    client.put_object(
        Bucket=request.bucket_name,
        Key=request.key,
        Body=request.data,
        ContentType=request.content_type
    )
    archive_url = f"https://{request.bucket_name}.s3.amazonaws.com/{request.key}"
    return ImageAssetArchiveResponse(archive_url=archive_url)
