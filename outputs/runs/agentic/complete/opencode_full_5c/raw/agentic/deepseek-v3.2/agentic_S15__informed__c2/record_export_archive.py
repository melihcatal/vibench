import os
import json
import tempfile
import zipfile
from datetime import datetime
from typing import Dict, Any, List, Optional
from google.cloud import storage


def archive_documents_to_storage(
    documents: List[Dict[str, Any]],
    bucket_name: str,
    archive_name: Optional[str] = None,
    format: str = "json",
) -> Dict[str, Any]:
    """
    Archive exported document snapshots to Google Cloud Storage.

    Args:
        documents: List of documents to archive
        bucket_name: Google Cloud Storage bucket name
        archive_name: Name for the archive file (optional, auto-generated if not provided)
        format: Archive format ("json", "jsonl", "csv")

    Returns:
        dict: Archive operation result
    """
    try:
        # Google Cloud credentials from environment variable
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )

        # Initialize Google Cloud Storage client
        client = storage.Client()

        # Generate archive name if not provided
        if not archive_name:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            archive_name = f"document_export_{timestamp}.zip"

        # Create temporary directory for archive preparation
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = os.path.join(temp_dir, archive_name)

            # Prepare documents based on format
            if format == "json":
                # Single JSON file with all documents
                data_file = os.path.join(temp_dir, "documents.json")
                with open(data_file, "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "exported_at": datetime.utcnow().isoformat(),
                            "document_count": len(documents),
                            "documents": documents,
                        },
                        f,
                        indent=2,
                        ensure_ascii=False,
                    )

                files_to_archive = [data_file]

            elif format == "jsonl":
                # JSON Lines format - one document per line
                data_file = os.path.join(temp_dir, "documents.jsonl")
                with open(data_file, "w", encoding="utf-8") as f:
                    for doc in documents:
                        json.dump(doc, f, ensure_ascii=False)
                        f.write("\n")

                files_to_archive = [data_file]

            elif format == "csv":
                # CSV format (simplified - for flat documents)
                import csv

                data_file = os.path.join(temp_dir, "documents.csv")

                # Extract all unique field names
                fieldnames = set()
                for doc in documents:
                    fieldnames.update(doc.keys())
                fieldnames = sorted(fieldnames)

                with open(data_file, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for doc in documents:
                        # Convert all values to strings for CSV
                        row = {
                            k: str(v) if v is not None else "" for k, v in doc.items()
                        }
                        writer.writerow(row)

                files_to_archive = [data_file]

            else:
                raise ValueError(f"Unsupported format: {format}")

            # Create metadata file
            metadata_file = os.path.join(temp_dir, "metadata.json")
            metadata = {
                "export_timestamp": datetime.utcnow().isoformat(),
                "document_count": len(documents),
                "format": format,
                "archive_name": archive_name,
                "generated_by": "record_export_archive.py",
            }

            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

            files_to_archive.append(metadata_file)

            # Create ZIP archive
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in files_to_archive:
                    arcname = os.path.basename(file_path)
                    zipf.write(file_path, arcname)

            # Upload to Google Cloud Storage
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(f"exports/{archive_name}")

            blob.upload_from_filename(archive_path)

            # Get public URL (if bucket is publicly accessible)
            # Note: In production, you might want to generate signed URLs instead
            public_url = (
                f"https://storage.googleapis.com/{bucket_name}/exports/{archive_name}"
            )

            # Get blob metadata
            blob.reload()

            return {
                "success": True,
                "archive_name": archive_name,
                "bucket": bucket_name,
                "document_count": len(documents),
                "format": format,
                "archive_size_bytes": blob.size,
                "created": blob.time_created.isoformat(),
                "public_url": public_url,
                "storage_class": blob.storage_class,
                "provider": "Google Cloud Storage",
                "metadata": metadata,
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Archive error: {str(e)}",
            "document_count": len(documents),
            "bucket": bucket_name,
            "format": format,
        }


def archive_single_document_with_attachments(
    document: Dict[str, Any],
    attachments: List[Dict[str, Any]],
    bucket_name: str,
    document_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Archive a single document with its attachments.

    Args:
        document: Document to archive
        attachments: List of attachment metadata/files
        bucket_name: Google Cloud Storage bucket name
        document_id: Document ID (optional, extracted from document if not provided)

    Returns:
        dict: Archive operation result
    """
    try:
        # Google Cloud credentials from environment variable
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )

        # Get document ID
        doc_id = document_id or document.get("_id", "unknown")

        # Initialize Google Cloud Storage client
        client = storage.Client()

        # Create temporary directory for archive preparation
        with tempfile.TemporaryDirectory() as temp_dir:
            archive_name = f"document_{doc_id}_archive_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.zip"
            archive_path = os.path.join(temp_dir, archive_name)

            # Save document as JSON
            doc_file = os.path.join(temp_dir, f"document_{doc_id}.json")
            with open(doc_file, "w", encoding="utf-8") as f:
                json.dump(document, f, indent=2, ensure_ascii=False)

            files_to_archive = [doc_file]

            # Process attachments
            attachment_info = []
            for i, attachment in enumerate(attachments):
                # This is a simplified example - in reality, attachments might be
                # base64 encoded data, file paths, or URLs to download
                if "filename" in attachment and "data" in attachment:
                    att_filename = attachment["filename"]
                    att_data = attachment["data"]

                    # Save attachment to temporary file
                    att_path = os.path.join(temp_dir, att_filename)

                    if isinstance(att_data, str) and att_data.startswith("base64:"):
                        # Handle base64 encoded data
                        import base64

                        b64_data = att_data[7:]  # Remove "base64:" prefix
                        with open(att_path, "wb") as f:
                            f.write(base64.b64decode(b64_data))
                    elif isinstance(att_data, bytes):
                        # Handle binary data
                        with open(att_path, "wb") as f:
                            f.write(att_data)
                    else:
                        # Handle text data
                        with open(att_path, "w", encoding="utf-8") as f:
                            f.write(str(att_data))

                    files_to_archive.append(att_path)
                    attachment_info.append(
                        {
                            "filename": att_filename,
                            "size_bytes": os.path.getsize(att_path),
                            "index": i,
                        }
                    )

            # Create metadata file
            metadata_file = os.path.join(temp_dir, "metadata.json")
            metadata = {
                "document_id": doc_id,
                "export_timestamp": datetime.utcnow().isoformat(),
                "attachment_count": len(attachments),
                "attachments": attachment_info,
                "archive_name": archive_name,
            }

            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

            files_to_archive.append(metadata_file)

            # Create ZIP archive
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for file_path in files_to_archive:
                    arcname = os.path.basename(file_path)
                    zipf.write(file_path, arcname)

            # Upload to Google Cloud Storage
            bucket = client.bucket(bucket_name)
            blob = bucket.blob(f"document_archives/{archive_name}")

            blob.upload_from_filename(archive_path)

            # Generate signed URL for temporary access (24 hours)
            # Note: This requires appropriate IAM permissions
            signed_url = blob.generate_signed_url(
                expiration=datetime.timedelta(hours=24), method="GET"
            )

            return {
                "success": True,
                "document_id": doc_id,
                "archive_name": archive_name,
                "bucket": bucket_name,
                "attachment_count": len(attachments),
                "archive_size_bytes": blob.size,
                "signed_url": signed_url,
                "expires_in": "24 hours",
                "created": blob.time_created.isoformat(),
                "provider": "Google Cloud Storage",
            }

    except Exception as e:
        return {
            "success": False,
            "error": f"Document archive error: {str(e)}",
            "document_id": doc_id,
            "bucket": bucket_name,
        }


def list_archives(bucket_name: str, prefix: str = "exports/") -> Dict[str, Any]:
    """
    List archived exports in Google Cloud Storage bucket.

    Args:
        bucket_name: Google Cloud Storage bucket name
        prefix: Prefix to filter archives

    Returns:
        dict: List of archives
    """
    try:
        # Google Cloud credentials from environment variable
        credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )

        # Initialize Google Cloud Storage client
        client = storage.Client()

        # List blobs in bucket with prefix
        bucket = client.bucket(bucket_name)
        blobs = list(bucket.list_blobs(prefix=prefix))

        archives = []
        for blob in blobs:
            if blob.name.endswith(".zip"):
                archives.append(
                    {
                        "name": blob.name,
                        "size_bytes": blob.size,
                        "created": blob.time_created.isoformat()
                        if blob.time_created
                        else None,
                        "updated": blob.updated.isoformat() if blob.updated else None,
                        "storage_class": blob.storage_class,
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
        return {
            "success": False,
            "error": f"Error listing archives: {str(e)}",
            "bucket": bucket_name,
            "prefix": prefix,
        }
