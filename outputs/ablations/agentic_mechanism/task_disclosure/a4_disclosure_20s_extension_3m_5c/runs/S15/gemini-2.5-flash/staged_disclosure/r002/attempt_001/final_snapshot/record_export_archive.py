import boto3
import os

def archive_document(file_path: str, bucket_name: str, object_name: str = None):
    """
    Archives a document snapshot or attachment in AWS S3.

    :param file_path: Path to the file to upload.
    :param bucket_name: S3 bucket name.
    :param object_name: S3 object name. If not specified, file_path is used.
    """
    if object_name is None:
        object_name = os.path.basename(file_path)

    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' successfully uploaded to '{bucket_name}/{object_name}'")
    except Exception as e:
        print(f"Error archiving file: {e}")

if __name__ == "__main__":
    # Example Usage: Replace with your actual file path and S3 bucket name
    # Ensure your AWS credentials are configured (e.g., via environment variables, AWS CLI, or IAM role)
    
    # Placeholder for the file to be archived
    local_file_to_archive = "path/to/your/document.pdf" 
    # Placeholder for your S3 bucket name
    s3_bucket = "your-s3-archive-bucket" 
    # Placeholder for the desired object name in S3 (optional, defaults to filename)
    s3_object_name = "archive/document_snapshot_2026-09-20.pdf" 
    
    # Create a dummy file for demonstration purposes if it doesn't exist
    if not os.path.exists(local_file_to_archive):
        os.makedirs(os.path.dirname(local_file_to_archive), exist_ok=True)
        with open(local_file_to_archive, "w") as f:
            f.write("This is a dummy document to be archived.")
        print(f"Created a dummy file: {local_file_to_archive}")

    archive_document(local_file_to_archive, s3_bucket, s3_object_name)
