from vision_client import VisionClient
from vision_models import ArchiveResult, ImageInput
import io
import mimetypes
import uuid

def archive_image_asset(
    image_input: ImageInput,
    file_name_prefix: str = "image-analysis-artifact",
    content_type: str = "application/octet-stream"
) -> ArchiveResult:
    client = VisionClient()
    s3_client = client.get_s3_client()
    bucket_name = client.get_aws_s3_bucket_name()

    if not bucket_name:
        raise ValueError("AWS_S3_BUCKET_NAME environment variable not set.")

    object_key = f"{file_name_prefix}-{uuid.uuid4()}"
    upload_data = None

    if image_input.image_url:
        # For simplicity, if it's a URL, we'll just store the URL in a text file.
        # In a real scenario, you might download the image first.
        object_key += ".txt"
        upload_data = image_input.image_url.encode('utf-8')
        content_type = "text/plain"
    elif image_input.image_base64:
        import base64
        decoded_image = base64.b64decode(image_input.image_base64)
        # Try to guess content type from magic bytes or default to jpeg
        # A more robust solution would be to pass content_type directly
        if decoded_image.startswith(b'\xff\xd8'):
            content_type = "image/jpeg"
            object_key += ".jpeg"
        elif decoded_image.startswith(b'\x89PNG\r\n\x1a\n'):
            content_type = "image/png"
            object_key += ".png"
        else:
            object_key += ".bin" # Generic binary
        
        upload_data = decoded_image
    else:
        raise ValueError("Either image_url or image_base64 must be provided for archiving.")

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=upload_data,
            ContentType=content_type
        )
        archive_url = f"https://{bucket_name}.s3.{client.aws_region_name}.amazonaws.com/{object_key}"
        return ArchiveResult(archive_url=archive_url, file_name=object_key)
    except Exception as e:
        raise RuntimeError(f"Failed to archive asset to S3: {e}")