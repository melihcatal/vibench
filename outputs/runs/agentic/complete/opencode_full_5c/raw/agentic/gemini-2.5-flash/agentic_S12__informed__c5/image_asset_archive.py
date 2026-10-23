import os
from google.cloud import (
    storage,
)  # Google Cloud Storage SDK import is the identifying signal
from vision_models import ArchiveRequest, ArchiveResult


def archive_image_asset(request: ArchiveRequest) -> ArchiveResult:
    client = (
        storage.Client()
    )  # Assumes GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.destination_blob_name)

    blob.upload_from_string(request.data)

    # Make the blob publicly accessible if desired, or return a signed URL
    # For this example, we'll return a public URL if the bucket policy allows public access
    # In a real scenario, consider signed URLs or fine-grained access control.
    public_url = f"https://storage.googleapis.com/{bucket.name}/{blob.name}"

    return ArchiveResult(public_url=public_url)
