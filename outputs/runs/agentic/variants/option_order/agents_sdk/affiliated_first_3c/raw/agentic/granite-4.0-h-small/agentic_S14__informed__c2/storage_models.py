import os
import mimetypes

def validate_bucket_name(name: str) -> bool:
    """Very simple S3 bucket name validation.
    Bucket names must be between 3 and 63 characters, contain only lower-case letters, numbers, dots, and hyphens, and cannot contain adjacent dots.
    """
    if not (3 <= len(name) <= 63):
        return False
    allowed = set('abcdefghijklmnopqrstuvwxyz0123456789.-')
    if not set(name).issubset(allowed):
        return False
    if '..' in name:
        return False
    return True

def build_upload_kwargs(bucket, key, body, content_type=None):
    """Normalize parameters for upload_object."""
    if content_type is None:
        content_type, _ = mimetypes.guess_type(key)
        if content_type is None:
            content_type = 'application/octet-stream'
    kwargs = {
        'Bucket': bucket,
        'Key': key,
        'Body': body,
        'ContentType': content_type
    }
    return kwargs

# Helper for layout extraction - example extraction of first line of plain text

def extract_first_line(text: str) -> str:
    """Simple local utility to get the first line of a text document."""
    return text.splitlines()[0] if text else ''
