import boto3
import os

def upload_object(bucket_name: str, object_name: str, file_path: str = None, data: bytes = None):
    """
    Uploads a file or byte stream to an S3 bucket.

    :param bucket_name: Name of the S3 bucket
    :param object_name: S3 object name (e.g., 'myfolder/myfile.txt')
    :param file_path: Path to the file to upload (optional)
    :param data: Byte stream to upload (optional)
    """
    # AWS S3 is the concrete external provider
    s3_client = boto3.client('s3')

    if file_path:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        try:
            s3_client.upload_file(file_path, bucket_name, object_name)
            print(f"File '{file_path}' uploaded to '{bucket_name}/{object_name}'")
        except Exception as e:
            print(f"Error uploading file: {e}")
    elif data is not None:
        try:
            s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=data)
            print(f"Byte stream uploaded to '{bucket_name}/{object_name}'")
        except Exception as e:
            print(f"Error uploading byte stream: {e}")
    else:
        raise ValueError("Either 'file_path' or 'data' must be provided.")

if __name__ == '__main__':
    # Example usage (replace with your actual bucket and object names)
    # Ensure you have AWS credentials configured (e.g., via environment variables or ~/.aws/credentials)

    # Example 1: Upload a file
    # Create a dummy file for testing
    with open("test_upload.txt", "w") as f:
        f.write("This is a test file for S3 upload.")

    # Uncomment the following lines to test file upload
    # BUCKET_NAME = "your-s3-bucket-name"
    # OBJECT_NAME_FILE = "test_folder/test_upload.txt"
    # FILE_TO_UPLOAD = "test_upload.txt"
    # upload_object(BUCKET_NAME, OBJECT_NAME_FILE, file_path=FILE_TO_UPLOAD)
    # os.remove("test_upload.txt") # Clean up dummy file

    # Example 2: Upload a byte stream
    # data_to_upload = b"This is a byte stream to upload to S3."
    # OBJECT_NAME_BYTES = "test_folder/test_bytes.txt"
    # upload_object(BUCKET_NAME, OBJECT_NAME_BYTES, data=data_to_upload)
