import boto3
import os

def archive_file_to_s3(file_path, bucket_name, object_name=None):
    """
    Archives a file to an AWS S3 bucket.

    :param file_path: Path to file to upload
    :param bucket_name: S3 bucket to upload to
    :param object_name: S3 object name. If not specified then file_path is used
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = os.path.basename(file_path)

    # Initialize S3 client (AWS SDK for Python)
    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"Error uploading file: {e}")
        return False

if __name__ == "__main__":
    # Example usage:
    # Replace with your actual file path and S3 bucket name
    # Ensure AWS credentials are configured (e.g., via environment variables, ~/.aws/credentials)
    # dummy_file_path = "path/to/your/document.pdf"
    # s3_bucket = "your-s3-bucket-name"

    # For demonstration, create a dummy file
    dummy_file_name = "example_document.txt"
    with open(dummy_file_name, "w") as f:
        f.write("This is a dummy document snapshot.")

    # Call the archiving function
    # archive_file_to_s3(dummy_file_name, s3_bucket)
    # print(f"To run this example, replace 'your-s3-bucket-name' with an actual S3 bucket and ensure AWS credentials are set up.")
    print(f"Dummy file '{dummy_file_name}' created. To archive, replace 'your-s3-bucket-name' and uncomment the archive_file_to_s3 call.")
