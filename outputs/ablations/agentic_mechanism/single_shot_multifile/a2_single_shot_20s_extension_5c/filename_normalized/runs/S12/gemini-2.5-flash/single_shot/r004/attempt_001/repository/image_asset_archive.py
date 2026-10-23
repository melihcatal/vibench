import os
import base64
import boto3
from vision_models import ArchiveRequest, ArchiveResult

def archive_image_asset(request: ArchiveRequest) -> ArchiveResult:
    client = boto3.client(
        's3',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    bucket_name = os.environ.get('AWS_S3_BUCKET_NAME')
    if not bucket_name:
        raise ValueError("AWS_S3_BUCKET_NAME environment variable not set.")

    object_key = request.filename
    upload_content = None
    content_type = 'application/octet-stream'

    if request.content_base64:
        upload_content = base64.b64decode(request.content_base64)
        # Infer content type from filename extension for common image formats
        if '.' in object_key:
            ext = object_key.split('.')[-1].lower()
            if ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']:
                content_type = f'image/{ext}'
            else:
                content_type = 'image/jpeg' # Default for general base64 images
        else:
            content_type = 'image/jpeg'
    elif request.text_content:
        upload_content = request.text_content.encode('utf-8')
        content_type = 'text/plain'

    if upload_content is None:
        raise ValueError("ArchiveRequest must contain either content_base64 or text_content.")

    extra_args = {'ContentType': content_type}
    if request.metadata:
        extra_args['Metadata'] = request.metadata

    client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=upload_content,
        **extra_args
    )

    archive_url = f"https://{bucket_name}.s3.{os.environ.get('AWS_REGION', 'us-east-1')}.amazonaws.com/{object_key}"

    return ArchiveResult(archive_url=archive_url, message=f"Asset '{object_key}' archived successfully.")