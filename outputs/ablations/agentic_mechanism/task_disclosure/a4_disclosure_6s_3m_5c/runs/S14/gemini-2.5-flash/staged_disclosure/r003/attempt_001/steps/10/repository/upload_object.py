
from google.cloud import storage
import os

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the Google Cloud Storage bucket."""
    # Instantiates a client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Create a blob (object) and upload the file
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")

def upload_byte_stream_to_gcs(bucket_name, data_bytes, destination_blob_name):
    """Uploads a byte stream to the Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(data_bytes, content_type='application/octet-stream')

    print(f"Byte stream uploaded to {destination_blob_name} in bucket {bucket_name}.")

if __name__ == "__main__":
    # Replace with your actual bucket name, file path, and desired blob name
    YOUR_BUCKET_NAME = "your-gcs-bucket-name" # e.g. "my-unique-bucket-123"
    YOUR_SOURCE_FILE = "path/to/your/local/file.txt" # e.g. "local_file.txt"
    YOUR_DESTINATION_BLOB = "desired/object/name.txt" # e.g. "cloud_file.txt"

    # Example usage for file upload
    # Uncomment and modify the following lines to test file upload
    # if os.path.exists(YOUR_SOURCE_FILE):
    #     upload_to_gcs(YOUR_BUCKET_NAME, YOUR_SOURCE_FILE, YOUR_DESTINATION_BLOB)
    # else:
    #     print(f"Error: Source file '{YOUR_SOURCE_FILE}' not found for upload_to_gcs.")

    # Example usage for byte stream upload
    # Uncomment and modify the following lines to test byte stream upload
    # BYTE_STREAM_DATA = b"This is some test data from a byte stream."
    # upload_byte_stream_to_gcs(YOUR_BUCKET_NAME, BYTE_STREAM_DATA, "byte_stream_data.txt")
