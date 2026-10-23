# upload_object.py
import os
from google.cloud import storage
from storage_models import UploadPayload, normalize_object_name
from storage_client import get_client, bucket_name

SERVICE = "Google Cloud Storage"

def upload(source_path: str, object_name: str, mime_type: str | None = None) -> str:
    """Upload a file or byte stream to the managed object storage bucket.\n    Returns the public object URL after successful upload."""
    client = get_client()
    bucket = client.bucket(bucket_name())
    blob = bucket.blob(normalize_object_name(object_name))
    # Determine mime type if not provided
def _detect_mime(path: str):
        import mimetypes
        return mimetypes.guess_type(path)[0] or "application/octet-stream"
    mime = mime_type or _detect_mime(source_path)
    # Upload either file path or bytes\n    if os.path.isfile(source_path):
        blob.upload_from_filename(source_path, content_type=mime)
    else:
        blob.upload_from_string(source_path, content_type=mime)
    # Generate signed URL for immediate download (30 days)
    # Note: Signed URLs require bucket IAM configuration.
    url = blob.generate_signed_url(version="v4", expiration=60 * 60 * 24 * 30)
    return url
