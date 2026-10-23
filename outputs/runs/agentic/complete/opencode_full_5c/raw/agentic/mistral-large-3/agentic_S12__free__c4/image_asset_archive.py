import os
from google.cloud import storage
from typing import Optional, Dict, Any
from datetime import datetime
import json


class ImageAssetArchiver:
    """Archives image-analysis artifacts and derived captions in Google Cloud Storage."""

    def __init__(self, bucket_name: Optional[str] = None):
        self.client = storage.Client()
        self.bucket_name = bucket_name or os.getenv("GCS_BUCKET_NAME")
        if not self.bucket_name:
            raise ValueError(
                "Bucket name must be provided or set in GCS_BUCKET_NAME environment variable."
            )
        self.bucket = self.client.bucket(self.bucket_name)

    def archive_analysis(
        self,
        image_name: str,
        analysis_results: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Archives image analysis results in Google Cloud Storage.

        Args:
            image_name: Name of the image file.
            analysis_results: Dictionary containing analysis results.
            metadata: Optional metadata to store with the analysis.

        Returns:
            URI of the archived analysis file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"analysis/{image_name}_{timestamp}.json"

        archive_data = {
            "timestamp": timestamp,
            "image_name": image_name,
            "analysis_results": analysis_results,
            "metadata": metadata or {},
        }

        blob = self.bucket.blob(archive_name)
        blob.upload_from_string(
            data=json.dumps(archive_data, indent=2), content_type="application/json"
        )

        return f"gs://{self.bucket_name}/{archive_name}"

    def archive_image(
        self,
        image_name: str,
        image_content: bytes,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Archives the original image in Google Cloud Storage.

        Args:
            image_name: Name of the image file.
            image_content: Raw image bytes.
            metadata: Optional metadata to store with the image.

        Returns:
            URI of the archived image file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"images/{image_name}_{timestamp}"

        blob = self.bucket.blob(archive_name)
        blob.upload_from_string(image_content)

        if metadata:
            blob.metadata = metadata
            blob.patch()

        return f"gs://{self.bucket_name}/{archive_name}"
