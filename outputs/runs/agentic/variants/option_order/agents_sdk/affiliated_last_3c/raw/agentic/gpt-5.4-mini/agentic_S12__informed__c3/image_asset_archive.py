from __future__ import annotations

import json

from google.cloud import storage

from vision_client import GoogleVisionClient, GoogleStorageArchive
from vision_models import ArchivePayload, VisionDescription


class ImageAssetArchiver:
    def __init__(self, bucket_name: str | None = None) -> None:
        self.archive = GoogleStorageArchive(bucket_name=bucket_name)
        self.storage_client = storage.Client()

    def run(self, object_key: str, description: VisionDescription, metadata: dict) -> str:
        body = json.dumps({"description": description.text, "metadata": metadata}).encode("utf-8")
        payload = ArchivePayload(object_key=object_key, metadata=metadata, body=body)
        return self.archive.upload(payload)
