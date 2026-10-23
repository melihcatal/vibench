import os
import json
from google.cloud import storage
from database_models import DocumentResponse, Document


def archive_document_snapshot(document: Document, bucket_name: str) -> DocumentResponse:
    client = storage.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    bucket = client.bucket(bucket_name)

    # Generate a unique blob name, e.g., using document ID and version
    blob_name = f"document_snapshots/{document.id}_v{document.version}.json"
    blob = bucket.blob(blob_name)

    try:
        # Convert the document to a JSON string and upload
        document_json = document.model_dump_json(by_alias=True, indent=2)
        blob.upload_from_string(document_json, content_type="application/json")
        public_url = blob.public_url
        document.content["archive_url"] = public_url
        return DocumentResponse(
            document=document, message=f"Document snapshot archived to {public_url}."
        )
    except Exception as e:
        return DocumentResponse(
            document=document,
            message=f"Failed to archive document snapshot to Google Cloud Storage: {e}",
        )
