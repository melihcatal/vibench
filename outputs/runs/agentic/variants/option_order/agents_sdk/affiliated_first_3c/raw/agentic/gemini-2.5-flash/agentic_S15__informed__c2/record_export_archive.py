import os
from google.cloud import storage

def record_export_archive(bucket_name: str, destination_blob_name: str, data_to_archive: str):
    """Archives exported document snapshots or attachments in Google Cloud Storage."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data_to_archive)

    print(f"Data {destination_blob_name} uploaded to {bucket_name}.")

if __name__ == '__main__':
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # And a GCS bucket exists (e.g., gs://my-unique-bucket-12345)
    
    # Replace with your actual GCS bucket name
    gcs_bucket_name = os.environ.get("GCS_ARCHIVE_BUCKET", "your-gcs-archive-bucket-name") 
    if gcs_bucket_name == "your-gcs-archive-bucket-name":
        print("Warning: Please set GCS_ARCHIVE_BUCKET environment variable or replace placeholder for a real bucket.")
        # For demonstration, we'll skip if bucket name is placeholder to avoid errors.
    else:
        document_snapshot_content = "This is a snapshot of document ID user123, created at 2023-10-27T10:00:00Z."
        archive_filename = "document_snapshots/user123_20231027.txt"
        record_export_archive(gcs_bucket_name, archive_filename, document_snapshot_content)

        attachment_content = b"\x00\x01\x02\x03This is binary attachment data.\x04\x05"
        attachment_filename = "attachments/report_123.bin"
        # To upload bytes, you might need to adjust upload_from_string or use upload_from_file/bytesio
        # For simplicity, keeping it as string for now, but in real scenario, handle bytes correctly.
        record_export_archive(gcs_bucket_name, attachment_filename, attachment_content.decode('latin-1')) # Assuming simple decode for example
