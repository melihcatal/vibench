import os
from google.cloud import storage
from typing import Dict, Any


class ArchiveRequest:
    def __init__(
        self,
        bucket_name: str,
        blob_name: str,
        content: str,
        content_type: str = "text/plain",
    ):
        self.bucket_name = bucket_name
        self.blob_name = blob_name
        self.content = content
        self.content_type = content_type


class ArchiveResponse:
    def __init__(self, public_url: str):
        self.public_url = public_url


def archive_image_analysis_artifact(request: ArchiveRequest) -> ArchiveResponse:
    client = storage.Client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.blob_name)

    blob.upload_from_string(request.content, content_type=request.content_type)

    # Make the blob publicly viewable (optional, depending on use case)
    # blob.make_public()

    return ArchiveResponse(public_url=blob.public_url)
