import os
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from google.cloud import storage


def archive_image_analysis(
    image_path: str,
    analysis_results: Dict[str, Any],
    bucket_name: str,
    credentials_path: str = None,
) -> Dict[str, Any]:
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    image_filename = os.path.basename(image_path)
    archive_id = str(uuid.uuid4())

    analysis_blob_name = f"analyses/{timestamp}_{archive_id}_analysis.json"
    analysis_blob = bucket.blob(analysis_blob_name)

    archive_data = {
        "archive_id": archive_id,
        "timestamp": timestamp,
        "image_filename": image_filename,
        "analysis_results": analysis_results,
        "metadata": {
            "source": "google-cloud-vision",
            "archive_service": "google-cloud-storage",
        },
    }

    analysis_blob.upload_from_string(
        json.dumps(archive_data, indent=2), content_type="application/json"
    )

    if os.path.exists(image_path):
        image_blob_name = f"images/{timestamp}_{archive_id}_{image_filename}"
        image_blob = bucket.blob(image_blob_name)
        image_blob.upload_from_filename(image_path)
    else:
        image_blob_name = None

    return {
        "archive_id": archive_id,
        "analysis_blob": analysis_blob_name,
        "image_blob": image_blob_name,
        "bucket": bucket_name,
        "timestamp": timestamp,
    }


def archive_captions_and_labels(
    captions: List[Dict[str, Any]],
    labels: List[Dict[str, Any]],
    description: str,
    bucket_name: str,
    credentials_path: str = None,
) -> Dict[str, Any]:
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    archive_id = str(uuid.uuid4())

    caption_data = {
        "archive_id": archive_id,
        "timestamp": timestamp,
        "description": description,
        "captions": captions,
        "labels": labels,
        "metadata": {
            "source": "google-cloud-vision",
            "archive_service": "google-cloud-storage",
        },
    }

    blob_name = f"captions/{timestamp}_{archive_id}_captions.json"
    blob = bucket.blob(blob_name)

    blob.upload_from_string(
        json.dumps(caption_data, indent=2), content_type="application/json"
    )

    return {
        "archive_id": archive_id,
        "blob_name": blob_name,
        "bucket": bucket_name,
        "timestamp": timestamp,
    }


def retrieve_analysis_archive(
    blob_name: str, bucket_name: str, credentials_path: str = None
) -> Dict[str, Any]:
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    content = blob.download_as_string()
    return json.loads(content)


def list_archived_analyses(
    bucket_name: str, prefix: str = "analyses/", credentials_path: str = None
) -> List[Dict[str, Any]]:
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix)

    archives = []
    for blob in blobs:
        archives.append(
            {
                "name": blob.name,
                "size": blob.size,
                "updated": blob.updated,
                "content_type": blob.content_type,
            }
        )

    return archives


def delete_archive(
    blob_name: str, bucket_name: str, credentials_path: str = None
) -> bool:
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    try:
        blob.delete()
        return True
    except Exception:
        return False
