import os
import json
import tempfile
import zipfile
from datetime import datetime
from typing import Dict, Any, List
from google.cloud import storage


def archive_documents_to_gcs(
    documents: List[Dict[str, Any]], bucket_name: str, prefix: str = "exports"
) -> Dict[str, Any]:
    """
    Archive exported document snapshots to Google Cloud Storage.

    Args:
        documents: List of documents to archive
        bucket_name: GCS bucket name
        prefix: Prefix for the archive file path

    Returns:
        dict: Archive result with GCS URL
    """
    # Check for Google credentials
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        return {
            "success": False,
            "error": "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set",
            "gcs_url": None,
        }

    if not documents:
        return {"success": False, "error": "No documents to archive", "gcs_url": None}

    # Create temporary directory for archive
    with tempfile.TemporaryDirectory() as temp_dir:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        archive_filename = f"document_export_{timestamp}.zip"
        archive_path = os.path.join(temp_dir, archive_filename)

        # Create ZIP archive
        try:
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Add metadata file
                metadata = {
                    "export_timestamp": timestamp,
                    "document_count": len(documents),
                    "export_format": "json",
                    "provider": "Google Cloud Storage",
                }

                metadata_content = json.dumps(metadata, indent=2)
                zipf.writestr("metadata.json", metadata_content)

                # Add each document as separate JSON file
                for i, doc in enumerate(documents):
                    doc_filename = f"document_{i + 1:04d}.json"
                    doc_content = json.dumps(doc, indent=2, default=str)
                    zipf.writestr(doc_filename, doc_content)

                # Add summary file
                summary = {
                    "total_documents": len(documents),
                    "document_ids": [
                        doc.get("_id", f"unknown_{i}")
                        for i, doc in enumerate(documents)
                    ],
                    "fields_present": list(
                        set().union(*[list(doc.keys()) for doc in documents])
                    ),
                }
                summary_content = json.dumps(summary, indent=2)
                zipf.writestr("summary.json", summary_content)

            # Upload to Google Cloud Storage
            client = storage.Client()
            bucket = client.bucket(bucket_name)

            # Create blob path
            blob_path = f"{prefix}/{archive_filename}" if prefix else archive_filename
            blob = bucket.blob(blob_path)

            # Upload the file
            blob.upload_from_filename(archive_path)

            # Make the blob publicly accessible (optional)
            # blob.make_public()

            gcs_url = f"gs://{bucket_name}/{blob_path}"

            return {
                "success": True,
                "gcs_url": gcs_url,
                "archive_filename": archive_filename,
                "document_count": len(documents),
                "archive_size": os.path.getsize(archive_path),
                "timestamp": timestamp,
                "provider": "Google Cloud Storage",
            }

        except Exception as e:
            return {"success": False, "error": str(e), "gcs_url": None}


def archive_single_document_with_attachments(
    document: Dict[str, Any],
    attachments: Dict[str, bytes],
    bucket_name: str,
    prefix: str = "attachments",
) -> Dict[str, Any]:
    """
    Archive a document with its attachments to GCS.

    Args:
        document: Document to archive
        attachments: Dictionary of attachment names to binary content
        bucket_name: GCS bucket name
        prefix: Prefix for the archive file path

    Returns:
        dict: Archive result
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        return {
            "success": False,
            "error": "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set",
            "gcs_url": None,
        }

    document_id = document.get("_id", "unknown")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    with tempfile.TemporaryDirectory() as temp_dir:
        archive_filename = f"document_{document_id}_{timestamp}.zip"
        archive_path = os.path.join(temp_dir, archive_filename)

        try:
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Add main document
                doc_content = json.dumps(document, indent=2, default=str)
                zipf.writestr("document.json", doc_content)

                # Add metadata
                metadata = {
                    "document_id": document_id,
                    "archive_timestamp": timestamp,
                    "attachment_count": len(attachments),
                    "attachment_names": list(attachments.keys()),
                    "provider": "Google Cloud Storage",
                }
                metadata_content = json.dumps(metadata, indent=2)
                zipf.writestr("metadata.json", metadata_content)

                # Add attachments
                for attachment_name, attachment_content in attachments.items():
                    zipf.writestr(f"attachments/{attachment_name}", attachment_content)

            # Upload to GCS
            client = storage.Client()
            bucket = client.bucket(bucket_name)

            blob_path = f"{prefix}/{archive_filename}" if prefix else archive_filename
            blob = bucket.blob(blob_path)
            blob.upload_from_filename(archive_path)

            gcs_url = f"gs://{bucket_name}/{blob_path}"

            return {
                "success": True,
                "gcs_url": gcs_url,
                "document_id": document_id,
                "archive_filename": archive_filename,
                "attachment_count": len(attachments),
                "archive_size": os.path.getsize(archive_path),
                "timestamp": timestamp,
                "provider": "Google Cloud Storage",
            }

        except Exception as e:
            return {"success": False, "error": str(e), "gcs_url": None}


def list_archives_in_bucket(
    bucket_name: str, prefix: str = "exports"
) -> Dict[str, Any]:
    """
    List archive files in a GCS bucket.

    Args:
        bucket_name: GCS bucket name
        prefix: Prefix to filter files

    Returns:
        dict: List of archive files
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        return {
            "success": False,
            "error": "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set",
            "archives": [],
        }

    try:
        client = storage.Client()
        bucket = client.bucket(bucket_name)

        archives = []
        blobs = bucket.list_blobs(prefix=prefix)

        for blob in blobs:
            if blob.name.endswith(".zip"):
                archives.append(
                    {
                        "name": blob.name,
                        "size": blob.size,
                        "updated": blob.updated.isoformat() if blob.updated else None,
                        "url": f"gs://{bucket_name}/{blob.name}",
                    }
                )

        return {
            "success": True,
            "bucket": bucket_name,
            "prefix": prefix,
            "archive_count": len(archives),
            "archives": archives,
            "provider": "Google Cloud Storage",
        }
    except Exception as e:
        return {"success": False, "error": str(e), "archives": []}
