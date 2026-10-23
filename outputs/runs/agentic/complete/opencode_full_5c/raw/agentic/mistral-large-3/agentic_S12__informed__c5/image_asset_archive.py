import os
from typing import Dict, Any, Optional
from datetime import datetime

from google.cloud import storage
from vision_models import Label, TextRegion, ImageDescription


def archive_image_analysis(
    image_bytes: bytes,
    labels: List[Label],
    text_regions: List[TextRegion],
    description: ImageDescription,
    bucket_name: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Dict[str, str]:
    """
    Archives image-analysis artifacts and derived captions in Google Cloud Storage.

    Args:
        image_bytes: Bytes of the original image.
        labels: List of detected labels.
        text_regions: List of detected text regions.
        description: Visual description of the image.
        bucket_name: Google Cloud Storage bucket name. If None, uses GCS_BUCKET_NAME.
        project_id: Google Cloud project ID. If None, uses GOOGLE_CLOUD_PROJECT.

    Returns:
        Dictionary containing URLs of archived artifacts.
    """
    bucket_name = bucket_name or os.getenv("GCS_BUCKET_NAME")
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")

    if not bucket_name or not project_id:
        raise ValueError(
            "Google Cloud Storage bucket name and project ID must be provided."
        )

    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_blob = bucket.blob(f"images/{timestamp}_image.jpg")
    labels_blob = bucket.blob(f"analysis/{timestamp}_labels.json")
    text_blob = bucket.blob(f"analysis/{timestamp}_text.json")
    description_blob = bucket.blob(f"analysis/{timestamp}_description.json")

    try:
        # Upload image
        image_blob.upload_from_string(image_bytes, content_type="image/jpeg")

        # Upload labels
        labels_data = [label.to_dict() for label in labels]
        labels_blob.upload_from_string(
            str(labels_data), content_type="application/json"
        )

        # Upload text regions
        text_data = [region.to_dict() for region in text_regions]
        text_blob.upload_from_string(str(text_data), content_type="application/json")

        # Upload description
        description_data = description.to_dict()
        description_blob.upload_from_string(
            str(description_data), content_type="application/json"
        )

        return {
            "image_url": image_blob.public_url,
            "labels_url": labels_blob.public_url,
            "text_url": text_blob.public_url,
            "description_url": description_blob.public_url,
        }

    except Exception as e:
        raise Exception(f"Google Cloud Storage error: {e}")
