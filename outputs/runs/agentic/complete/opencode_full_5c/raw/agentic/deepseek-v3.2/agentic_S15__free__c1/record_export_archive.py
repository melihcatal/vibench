import os
import json
import zipfile
import tempfile
from datetime import datetime
from typing import Dict, Any, List, Optional
from google.cloud import storage


def record_export_archive(
    documents: List[Dict[str, Any]],
    bucket_name: str = None,
    archive_name: str = None,
    format_type: str = "json",
) -> Dict[str, Any]:
    """
    Archive exported document snapshots in Google Cloud Storage.

    Args:
        documents: List of document records to archive
        bucket_name: Google Cloud Storage bucket name
        archive_name: Name for the archive file
        format_type: Archive format ('json', 'zip')

    Returns:
        dict: Archive operation result
    """
    try:
        # Initialize Google Cloud Storage client
        storage_client = storage.Client()

        # Use default bucket name if not provided
        if not bucket_name:
            bucket_name = os.environ.get("GCS_BUCKET_NAME", "document-archives")

        # Generate archive name if not provided
        if not archive_name:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            archive_name = f"document_export_{timestamp}"

        # Create temporary directory for archive preparation
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = os.path.join(temp_dir, f"{archive_name}.{format_type}")

            if format_type == "json":
                # Create JSON archive
                archive_data = {
                    "export_timestamp": datetime.utcnow().isoformat() + "Z",
                    "document_count": len(documents),
                    "documents": documents,
                }

                with open(archive_path, "w", encoding="utf-8") as f:
                    json.dump(archive_data, f, indent=2, ensure_ascii=False)

                file_size = os.path.getsize(archive_path)

            elif format_type == "zip":
                # Create ZIP archive with individual JSON files
                with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                    # Add metadata file
                    metadata = {
                        "export_timestamp": datetime.utcnow().isoformat() + "Z",
                        "document_count": len(documents),
                        "format": "individual_json_files",
                    }

                    metadata_path = os.path.join(temp_dir, "metadata.json")
                    with open(metadata_path, "w") as f:
                        json.dump(metadata, f, indent=2)
                    zipf.write(metadata_path, "metadata.json")

                    # Add each document as separate JSON file
                    for i, doc in enumerate(documents):
                        doc_filename = f"document_{i:04d}.json"
                        doc_path = os.path.join(temp_dir, doc_filename)

                        with open(doc_path, "w") as f:
                            json.dump(doc, f, indent=2)

                        zipf.write(doc_path, doc_filename)

                file_size = os.path.getsize(archive_path)

            else:
                return {
                    "success": False,
                    "error": f"Unsupported format type: {format_type}",
                    "provider": "google:cloud-storage",
                }

            # Upload to Google Cloud Storage
            bucket = storage_client.bucket(bucket_name)

            # Check if bucket exists, create if not
            try:
                bucket = storage_client.get_bucket(bucket_name)
            except Exception:
                # Bucket doesn't exist, create it
                bucket = storage_client.create_bucket(bucket_name)

            # Upload the file
            blob_name = f"{archive_name}.{format_type}"
            blob = bucket.blob(blob_name)

            blob.upload_from_filename(archive_path)

            # Get public URL (if bucket is publicly accessible)
            blob.make_public()
            public_url = blob.public_url

            # Get blob metadata
            blob.reload()

            return {
                "success": True,
                "archive_info": {
                    "name": archive_name,
                    "format": format_type,
                    "file_size_bytes": file_size,
                    "file_size_mb": round(file_size / (1024 * 1024), 2),
                    "document_count": len(documents),
                    "bucket": bucket_name,
                    "blob_name": blob_name,
                    "public_url": public_url,
                    "storage_class": blob.storage_class,
                    "created": blob.time_created.isoformat(),
                    "updated": blob.updated.isoformat(),
                    "md5_hash": blob.md5_hash,
                },
                "provider": "google:cloud-storage",
                "service": "storage.Client",
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "google:cloud-storage",
            "service": "storage.Client",
        }


def export_documents_to_gcs(
    documents: List[Dict[str, Any]], bucket_name: str, prefix: str = "exports/"
) -> Dict[str, Any]:
    """
    Export documents to Google Cloud Storage as individual files.

    Args:
        documents: List of documents to export
        bucket_name: GCS bucket name
        prefix: Path prefix for stored files

    Returns:
        dict: Export operation result
    """
    try:
        storage_client = storage.Client()

        # Get or create bucket
        try:
            bucket = storage_client.get_bucket(bucket_name)
        except Exception:
            bucket = storage_client.create_bucket(bucket_name)

        exported_files = []

        for i, document in enumerate(documents):
            # Generate filename
            doc_id = document.get("id", f"doc_{i:04d}")
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{prefix}{doc_id}_{timestamp}.json"

            # Create blob and upload
            blob = bucket.blob(filename)

            # Prepare document data with metadata
            export_data = {
                "export_timestamp": datetime.utcnow().isoformat() + "Z",
                "document": document,
                "export_metadata": {
                    "document_index": i,
                    "total_documents": len(documents),
                },
            }

            # Upload as JSON
            blob.upload_from_string(
                json.dumps(export_data, indent=2), content_type="application/json"
            )

            # Make publicly accessible
            blob.make_public()

            exported_files.append(
                {
                    "document_id": doc_id,
                    "filename": filename,
                    "blob_name": blob.name,
                    "public_url": blob.public_url,
                    "size_bytes": len(json.dumps(export_data).encode("utf-8")),
                }
            )

        return {
            "success": True,
            "exported_files": exported_files,
            "summary": {
                "total_documents": len(documents),
                "successful_exports": len(exported_files),
                "bucket": bucket_name,
                "prefix": prefix,
                "export_timestamp": datetime.utcnow().isoformat() + "Z",
            },
            "provider": "google:cloud-storage",
            "service": "storage.Client",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "google:cloud-storage",
            "service": "storage.Client",
        }


def create_backup_archive(
    documents: List[Dict[str, Any]], backup_name: str = None
) -> Dict[str, Any]:
    """
    Create a backup archive of documents with versioning.

    Args:
        documents: Documents to backup
        backup_name: Name for the backup

    Returns:
        dict: Backup operation result
    """
    try:
        storage_client = storage.Client()

        # Generate backup name
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        if not backup_name:
            backup_name = f"backup_{timestamp}"

        bucket_name = os.environ.get("GCS_BACKUP_BUCKET", "document-backups")

        # Create temporary backup file
        with tempfile.TemporaryDirectory() as temp_dir:
            backup_path = os.path.join(temp_dir, f"{backup_name}.zip")

            # Create ZIP archive
            with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                # Add main data file
                data = {
                    "backup_timestamp": datetime.utcnow().isoformat() + "Z",
                    "backup_name": backup_name,
                    "document_count": len(documents),
                    "documents": documents,
                }

                data_path = os.path.join(temp_dir, "data.json")
                with open(data_path, "w") as f:
                    json.dump(data, f, indent=2)
                zipf.write(data_path, "data.json")

                # Add manifest file
                manifest = {
                    "version": "1.0",
                    "created": datetime.utcnow().isoformat() + "Z",
                    "format": "zip",
                    "compression": "deflated",
                    "file_count": 1,
                    "total_documents": len(documents),
                }

                manifest_path = os.path.join(temp_dir, "manifest.json")
                with open(manifest_path, "w") as f:
                    json.dump(manifest, f, indent=2)
                zipf.write(manifest_path, "manifest.json")

            # Upload to GCS
            try:
                bucket = storage_client.get_bucket(bucket_name)
            except Exception:
                bucket = storage_client.create_bucket(bucket_name)

            blob_name = f"backups/{backup_name}.zip"
            blob = bucket.blob(blob_name)

            blob.upload_from_filename(backup_path)

            file_size = os.path.getsize(backup_path)

            return {
                "success": True,
                "backup_info": {
                    "name": backup_name,
                    "bucket": bucket_name,
                    "blob_name": blob_name,
                    "file_size_bytes": file_size,
                    "document_count": len(documents),
                    "created": datetime.utcnow().isoformat() + "Z",
                    "storage_location": f"gs://{bucket_name}/{blob_name}",
                },
                "provider": "google:cloud-storage",
                "service": "storage.Client",
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "google:cloud-storage",
            "service": "storage.Client",
        }
