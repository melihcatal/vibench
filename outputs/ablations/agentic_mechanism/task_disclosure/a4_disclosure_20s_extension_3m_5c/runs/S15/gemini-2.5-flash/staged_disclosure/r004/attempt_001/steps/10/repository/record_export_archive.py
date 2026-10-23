
import boto3
import os

def archive_to_s3(file_path, bucket_name, object_name=None):
    """
    Archives a file to an Amazon S3 bucket.

    :param file_path: Path to the file to upload.
    :param bucket_name: Name of the S3 bucket.
    :param object_name: S3 object name. If not specified then file_path is used.
    :return: True if file was uploaded, else False.
    """
    
    # Ensure AWS credentials and region are configured, e.g., via environment variables
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
    
    s3_client = boto3.client('s3')

    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File '{file_path}' uploaded to '{bucket_name}/{object_name}'")
        return True
    except Exception as e:
        print(f"Error archiving file to S3: {e}")
        return False

if __name__ == "__main__":
    # Example Usage:
    # IMPORTANT: Replace with your actual file path, bucket name, and configure AWS credentials.
    
    # Create a dummy file for demonstration
    dummy_file_path = "document_snapshot.txt"
    with open(dummy_file_path, "w") as f:
        f.write("This is a dummy document snapshot content.")
    
    your_file_to_archive = dummy_file_path  # Replace with the actual path to your document/attachment
    your_s3_bucket_name = "your-unique-s3-bucket-name"  # Replace with your actual S3 bucket name

    # The object name in S3. If not provided, the base name of the file path will be used.
    your_s3_object_name = "archives/document_snapshot_20260920.txt" 

    print(f"Attempting to archive '{your_file_to_archive}' to S3 bucket '{your_s3_bucket_name}'...")
    if archive_to_s3(your_file_to_archive, your_s3_bucket_name, your_s3_object_name):
        print("Archiving successful!")
    else:
        print("Archiving failed.")

    # Clean up the dummy file
    os.remove(dummy_file_path)

# To run this code, you need to install the boto3 library:
# pip install boto3
