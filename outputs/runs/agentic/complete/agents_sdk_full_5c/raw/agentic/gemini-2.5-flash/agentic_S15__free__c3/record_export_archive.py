from typing import Dict, Any, Optional
from google.cloud import storage
import json
import datetime

def archive_document_snapshot(document_id: str, document_data: Dict[str, Any], bucket_name: str, project_id: str) -> Optional[str]:
    """Archives a document snapshot (JSON content) to a Google Cloud Storage bucket.

    The snapshot is stored as a JSON file with a timestamped name in the specified bucket.

    Args:
        document_id (str): The ID of the document being archived.
        document_data (Dict[str, Any]): The JSON content of the document snapshot.
        bucket_name (str): The name of the Google Cloud Storage bucket.
        project_id (str): Your Google Cloud project ID.

    Returns:
        Optional[str]: The full GCS path (gs://bucket_name/object_name) of the archived object if successful, None otherwise.
    """
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)

    # Generate a unique object name with timestamp
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")
    object_name = f"document_archives/{document_id}_{timestamp}.json"

    blob = bucket.blob(object_name)

    try:
        # Convert dictionary to JSON string and upload
        json_content = json.dumps(document_data, indent=2)
        blob.upload_from_string(json_content, content_type="application/json")
        gcs_path = f"gs://{bucket_name}/{object_name}"
        print(f"Document {document_id} archived successfully to GCS: {gcs_path}")
        return gcs_path
    except Exception as e:
        print(f"Error archiving document {document_id} to GCS bucket {bucket_name}: {e}")
        return None

if __name__ == "__main__":
    # Example Usage:
    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # Replace 'your-gcs-bucket-name' with the name of an existing GCS bucket.
    # Ensure you have enabled the Cloud Storage API and have appropriate permissions.
    # For local execution, ensure gcloud is authenticated or GOOGLE_APPLICATION_CREDENTIALS is set.
    GCP_PROJECT_ID = "your-gcp-project-id"         # <<< IMPORTANT: Update this to your GCP Project ID
    GCS_BUCKET_NAME = "your-gcs-bucket-name" # <<< IMPORTANT: Update this to your GCS Bucket Name

    sample_doc_id = "archive_prod_123"
    sample_doc_data = {
        "name": "Archived Product Snapshot",
        "sku": "AP-12345",
        "price": 10.50,
        "status": "discontinued",
        "archive_date": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    print("\nAttempting to archive document snapshot to GCS...")
    try:
        archive_path = archive_document_snapshot(
            sample_doc_id, sample_doc_data, GCS_BUCKET_NAME, GCP_PROJECT_ID
        )

        if archive_path:
            print(f"Archived document available at: {archive_path}")
            # You can verify this by checking your GCS bucket in the Cloud Console
        else:
            print("Failed to archive document snapshot.")

    except Exception as e:
        print(f"Example usage failed: {e}")
