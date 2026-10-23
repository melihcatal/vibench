import boto3
import os

def archive_to_s3(file_path, bucket_name, object_name=None):
    """
    Archives a file to an Amazon S3 bucket.

    :param file_path: Path to file to upload
    :param bucket_name: S3 Bucket to upload to
    :param object_name: S3 object name. If not specified then file_path is used
    :return: True if file was uploaded, else False
    """
    # AWS S3 client
    # Ensure your AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    # and region (AWS_DEFAULT_REGION) are configured in your environment
    # or AWS configuration files.
    s3_client = boto3.client('s3')

    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"'{file_path}' successfully uploaded to '{bucket_name}/{object_name}'")
        return True
    except Exception as e:
        print(f"Error uploading '{file_path}': {e}")
        return False

if __name__ == "__main__":
    # Example Usage:
    # Replace 'your-file-to-archive.txt' with the actual path to your document snapshot or attachment
    # Replace 'your-s3-bucket-name' with the name of your S3 bucket
    # Replace 'archive/document_snapshot_2023-10-27.txt' with your desired S3 object key
    
    # Create a dummy file for demonstration
    dummy_file_path = "document_snapshot.txt"
    with open(dummy_file_path, "w") as f:
        f.write("This is a dummy document snapshot content.")

    # These would typically come from environment variables or a configuration file
    # For demonstration, hardcoding them here. DO NOT hardcode sensitive credentials in production code.
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "your-s3-bucket-name")
    FILE_TO_ARCHIVE = dummy_file_path # The file you want to archive
    S3_OBJECT_KEY = os.environ.get("S3_OBJECT_KEY", "exported_documents/document_snapshot.txt") # Desired path in S3

    if archive_to_s3(FILE_TO_ARCHIVE, S3_BUCKET_NAME, S3_OBJECT_KEY):
        print("Archiving task completed.")
    else:
        print("Archiving task failed.")
    
    # Clean up dummy file
    os.remove(dummy_file_path)
