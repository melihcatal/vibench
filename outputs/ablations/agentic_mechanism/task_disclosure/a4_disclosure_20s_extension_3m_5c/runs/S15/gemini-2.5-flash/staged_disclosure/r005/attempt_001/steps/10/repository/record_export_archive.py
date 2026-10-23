import boto3
import os

def archive_document(file_path, bucket_name, object_name=None):
    """
    Archives a document (snapshot or attachment) to AWS S3.

    :param file_path: Path to the file to upload.
    :param bucket_name: S3 bucket name.
    :param object_name: S3 object name. If not specified, file_path basename is used.
    :return: True if file was uploaded, else False.
    """
    if object_name is None:
        object_name = os.path.basename(file_path)

    # AWS S3 client
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set in your environment
    # or configured via ~/.aws/credentials
    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return False

if __name__ == "__main__":
    # Example Usage:
    # Create a dummy file for demonstration
    dummy_file_name = "example_document.txt"
    with open(dummy_file_name, "w") as f:
        f.write("This is a dummy document to be archived.")

    # Replace with your actual S3 bucket name
    S3_BUCKET_NAME = "your-s3-bucket-name" 

    # Replace with the path to the document you want to archive
    DOCUMENT_TO_ARCHIVE = dummy_file_name 

    if archive_document(DOCUMENT_TO_ARCHIVE, S3_BUCKET_NAME):
        print(f"Document {DOCUMENT_TO_ARCHIVE} successfully archived.")
    else:
        print(f"Failed to archive document {DOCUMENT_TO_ARCHIVE}.")

    # Clean up the dummy file
    os.remove(dummy_file_name)
