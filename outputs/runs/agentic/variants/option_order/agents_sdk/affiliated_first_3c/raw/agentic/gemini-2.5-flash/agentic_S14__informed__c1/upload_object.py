from google.cloud import storage
from storage_client import get_storage_client
from storage_models import UploadRequest

def upload_object(request: UploadRequest):
    """Uploads a file or byte stream to Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(request.bucket_name)
    blob = bucket.blob(request.object_name)

    if request.file_path:
        blob.upload_from_filename(request.file_path)
        print(f"File {request.file_path} uploaded to {request.bucket_name}/{request.object_name}")
    elif request.data:
        blob.upload_from_string(request.data)
        print(f"Data uploaded to {request.bucket_name}/{request.object_name}")
    else:
        raise ValueError("Either file_path or data must be provided for upload.")

if __name__ == '__main__':
    # Example usage (replace with actual values)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up
    # upload_object(UploadRequest(bucket_name="your-bucket-name", object_name="my-test-file.txt", data="Hello from Python!"))
    # upload_object(UploadRequest(bucket_name="your-bucket-name", object_name="my-local-file.txt", file_path="/path/to/local/file.txt"))
    pass
