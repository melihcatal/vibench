import os
import json
import zipfile
import tempfile
from datetime import datetime
from typing import Dict, Any, List
from google.cloud import storage


def archive_document_snapshots(
    documents: List[Dict[str, Any]], bucket_name: str = None, archive_name: str = None
) -> Dict[str, Any]:
    """
    Archive exported document snapshots or attachments in Google Cloud Storage.

    Args:
        documents: List of document records to archive
        bucket_name: Google Cloud Storage bucket name
        archive_name: Name for the archive file (optional)

    Returns:
        dict: Archive results
    """
    try:
        # Get bucket name from environment or parameter
        bucket_name = bucket_name or os.environ.get("GCS_BUCKET_NAME")
        if not bucket_name:
            return {
                "success": False,
                "error": "No Google Cloud Storage bucket specified",
            }

        # Generate archive name if not provided
        if not archive_name:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            archive_name = f"document_archive_{timestamp}.zip"

        # Initialize Google Cloud Storage client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        # Create temporary directory for archive
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = os.path.join(temp_dir, archive_name)

            # Create ZIP archive
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for i, doc in enumerate(documents):
                    doc_id = doc.get("id", f"doc_{i}")
                    doc_data = doc.get("data", {})

                    # Create JSON file for each document
                    doc_filename = f"{doc_id}.json"
                    doc_content = json.dumps(
                        {
                            "id": doc_id,
                            "data": doc_data,
                            "metadata": doc.get("metadata", {}),
                            "exported_at": datetime.utcnow().isoformat(),
                        },
                        indent=2,
                    )

                    # Add to ZIP
                    zipf.writestr(doc_filename, doc_content)

            # Upload to Google Cloud Storage
            blob = bucket.blob(archive_name)
            blob.upload_from_filename(archive_path)

            # Get blob metadata
            blob.reload()

            return {
                "success": True,
                "archive_name": archive_name,
                "bucket_name": bucket_name,
                "document_count": len(documents),
                "archive_size": blob.size,
                "archive_url": f"gs://{bucket_name}/{archive_name}",
                "public_url": blob.public_url,
                "md5_hash": blob.md5_hash,
                "created": blob.time_created.isoformat(),
                "service_used": "google-cloud-storage",
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "service_used": "google-cloud-storage",
        }


def export_documents_to_gcs(
    documents: List[Dict[str, Any]], bucket_name: str = None, prefix: str = "exports/"
) -> Dict[str, Any]:
    """
    Export documents as individual JSON files to Google Cloud Storage.

    Args:
        documents: List of document records to export
        bucket_name: Google Cloud Storage bucket name
        prefix: Path prefix for exported files

    Returns:
        dict: Export results
    """
    try:
        bucket_name = bucket_name or os.environ.get("GCS_BUCKET_NAME")
        if not bucket_name:
            return {
                "success": False,
                "error": "No Google Cloud Storage bucket specified",
            }

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        export_results = []
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        for doc in documents:
            doc_id = doc.get("id", "unknown")
            doc_data = doc.get("data", {})

            # Create filename
            filename = f"{prefix}{doc_id}_{timestamp}.json"

            # Prepare document content
            doc_content = json.dumps(
                {
                    "id": doc_id,
                    "data": doc_data,
                    "metadata": doc.get("metadata", {}),
                    "exported_at": datetime.utcnow().isoformat(),
                },
                indent=2,
            )

            # Upload to GCS
            blob = bucket.blob(filename)
            blob.upload_from_string(doc_content, content_type="application/json")

            export_results.append(
                {
                    "document_id": doc_id,
                    "filename": filename,
                    "size": len(doc_content),
                    "url": f"gs://{bucket_name}/{filename}",
                }
            )

        return {
            "success": True,
            "exports": export_results,
            "bucket_name": bucket_name,
            "prefix": prefix,
            "export_count": len(documents),
            "timestamp": timestamp,
            "service_used": "google-cloud-storage",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "service_used": "google-cloud-storage",
        }


def create_incremental_backup(
    documents: List[Dict[str, Any]], backup_type: str = "daily"
) -> Dict[str, Any]:
    """
    Create incremental backup of documents to Google Cloud Storage.

    Args:
        documents: List of document records to backup
        backup_type: Type of backup ('daily', 'weekly', 'monthly')

    Returns:
        dict: Backup results
    """
    try:
        bucket_name = os.environ.get("GCS_BACKUP_BUCKET_NAME") or os.environ.get(
            "GCS_BUCKET_NAME"
        )
        if not bucket_name:
            return {
                "success": False,
                "error": "No Google Cloud Storage bucket specified for backups",
            }

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_prefix = f"backups/{backup_type}/{timestamp}/"

        return export_documents_to_gcs(
            documents=documents, bucket_name=bucket_name, prefix=backup_prefix
        )

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "service_used": "google-cloud-storage",
        }


def list_archives(bucket_name: str = None, prefix: str = "") -> Dict[str, Any]:
    """
    List available archives in Google Cloud Storage.

    Args:
        bucket_name: Google Cloud Storage bucket name
        prefix: Path prefix to filter archives

    Returns:
        dict: List of archives
    """
    try:
        bucket_name = bucket_name or os.environ.get("GCS_BUCKET_NAME")
        if not bucket_name:
            return {
                "success": False,
                "error": "No Google Cloud Storage bucket specified",
            }

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        archives = []
        blobs = bucket.list_blobs(prefix=prefix)

        for blob in blobs:
            if blob.name.endswith(".zip") or "archive" in blob.name.lower():
                archives.append(
                    {
                        "name": blob.name,
                        "size": blob.size,
                        "updated": blob.updated.isoformat(),
                        "url": f"gs://{bucket_name}/{blob.name}",
                    }
                )

        return {
            "success": True,
            "archives": archives,
            "count": len(archives),
            "bucket_name": bucket_name,
            "prefix": prefix,
            "service_used": "google-cloud-storage",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "service_used": "google-cloud-storage",
        }


def download_archive(
    archive_name: str, bucket_name: str = None, download_path: str = None
) -> Dict[str, Any]:
    """
    Download an archive from Google Cloud Storage.

    Args:
        archive_name: Name of the archive to download
        bucket_name: Google Cloud Storage bucket name
        download_path: Local path to save the archive

    Returns:
        dict: Download results
    """
    try:
        bucket_name = bucket_name or os.environ.get("GCS_BUCKET_NAME")
        if not bucket_name:
            return {
                "success": False,
                "error": "No Google Cloud Storage bucket specified",
            }

        if not download_path:
            download_path = archive_name

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(archive_name)

        blob.download_to_filename(download_path)

        return {
            "success": True,
            "archive_name": archive_name,
            "download_path": download_path,
            "size": os.path.getsize(download_path),
            "bucket_name": bucket_name,
            "service_used": "google-cloud-storage",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "service_used": "google-cloud-storage",
        }
