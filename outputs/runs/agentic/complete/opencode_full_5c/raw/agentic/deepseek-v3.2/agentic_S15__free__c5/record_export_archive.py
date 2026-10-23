import os
import json
import tempfile
import zipfile
from datetime import datetime
from typing import List, Dict, Any
from google.cloud import storage


def record_export_archive(
    documents: List[Dict[str, Any]],
    bucket_name: str = None,
    archive_prefix: str = "document_export",
) -> str:
    """
    Archive exported document snapshots in Google Cloud Storage.

    Args:
        documents: List of documents to archive
        bucket_name: GCS bucket name (defaults from environment)
        archive_prefix: Prefix for archive filename

    Returns:
        str: GCS URL of the archived file
    """
    if bucket_name is None:
        bucket_name = os.environ.get("GCS_BUCKET_NAME", "document-archives")

    # Initialize Google Cloud Storage client
    storage_client = storage.Client.from_service_account_json(
        os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    )

    # Create a temporary directory for archive preparation
    with tempfile.TemporaryDirectory() as temp_dir:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        archive_filename = f"{archive_prefix}_{timestamp}.zip"
        archive_path = os.path.join(temp_dir, archive_filename)

        # Create ZIP archive
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add metadata file
            metadata = {
                "export_timestamp": timestamp,
                "document_count": len(documents),
                "archive_format": "zip",
                "compression": "deflated",
            }

            metadata_path = os.path.join(temp_dir, "metadata.json")
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)

            zipf.write(metadata_path, "metadata.json")

            # Add individual documents as JSON files
            for i, doc in enumerate(documents):
                doc_id = doc.get("id", doc.get("document_id", f"document_{i}"))
                doc_filename = f"documents/{doc_id}.json"
                doc_path = os.path.join(temp_dir, f"{doc_id}.json")

                with open(doc_path, "w") as f:
                    json.dump(doc, f, indent=2)

                zipf.write(doc_path, doc_filename)

            # Add summary file
            summary = {
                "total_documents": len(documents),
                "document_ids": [
                    doc.get("id", doc.get("document_id", f"document_{i}"))
                    for i, doc in enumerate(documents)
                ],
                "field_summary": {},
            }

            # Analyze common fields
            if documents:
                sample_doc = documents[0]
                for field in sample_doc.keys():
                    field_types = set()
                    for doc in documents:
                        if field in doc:
                            field_types.add(type(doc[field]).__name__)
                    summary["field_summary"][field] = {
                        "present_in": sum(1 for doc in documents if field in doc),
                        "types": list(field_types),
                    }

            summary_path = os.path.join(temp_dir, "summary.json")
            with open(summary_path, "w") as f:
                json.dump(summary, f, indent=2)

            zipf.write(summary_path, "summary.json")

        # Upload to Google Cloud Storage
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f"archives/{archive_filename}")

        with open(archive_path, "rb") as f:
            blob.upload_from_file(f)

        # Set blob metadata
        blob.metadata = {
            "document_count": str(len(documents)),
            "export_timestamp": timestamp,
            "archive_type": "document_export",
        }
        blob.patch()

        # Make blob publicly accessible (optional, based on requirements)
        # blob.make_public()

        # Return GCS URL
        gcs_url = f"gs://{bucket_name}/archives/{archive_filename}"
        return gcs_url
