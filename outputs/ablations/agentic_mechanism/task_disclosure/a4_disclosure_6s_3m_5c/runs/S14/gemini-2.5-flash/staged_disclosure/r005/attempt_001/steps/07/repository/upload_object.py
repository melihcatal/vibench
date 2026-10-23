import boto3
import os

def upload_object(bucket_name: str, object_name: str, file_path: str = None, data_stream: bytes = None):
    """
    Uploads a file or byte stream to an S3 bucket.

    :param bucket_name: Name of the S3 bucket
    :param object_name: S3 object name (e.g., 'myfolder/myfile.txt')
    :param file_path: Path to the file to upload (optional)
    :param data_stream: Byte stream to upload (optional)
    :return: True if upload was successful, False otherwise
    """
    s3_client = boto3.client('s3')

    if file_path:
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return False
        try:
            s3_client.upload_file(file_path, bucket_name, object_name)
            print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
            return True
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False
    elif data_stream is not None:
        try:
            s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=data_stream)
            print(f"Byte stream uploaded to {bucket_name}/{object_name}")
            return True
        except Exception as e:
            print(f"Error uploading byte stream: {e}")
            return False
    else:
        print("Error: Either file_path or data_stream must be provided.")
        return False

if __name__ == '__main__':
    # Example usage (requires AWS credentials configured and an S3 bucket)
    # bucket_name = "your-s3-bucket-name"
    # object_key_file = "test_upload_file.txt"
    # object_key_stream = "test_upload_stream.txt"

    # Create a dummy file for upload
    # with open("dummy_file.txt", "w") as f:
    #     f.write("This is a test file for S3 upload.")

    # Example 1: Upload a file
    # if upload_object(bucket_name, object_key_file, file_path="dummy_file.txt"):
    #     print("File upload successful!")
    # else:
    #     print("File upload failed.")

    # Example 2: Upload a byte stream
    # byte_data = b"This is a test byte stream for S3 upload."
    # if upload_object(bucket_name, object_key_stream, data_stream=byte_data):
    #     print("Byte stream upload successful!")
    # else:
    #     print("Byte stream upload failed.")

    # Clean up dummy file
    # if os.path.exists("dummy_file.txt"):
    #     os.remove("dummy_file.txt")
    pass
