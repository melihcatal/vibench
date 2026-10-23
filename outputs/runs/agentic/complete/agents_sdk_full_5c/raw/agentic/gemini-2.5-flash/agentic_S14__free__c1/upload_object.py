import os
import boto3

def upload_object(bucket_name: str, object_name: str, file_path: str):
    """
    Uploads a file to an S3 bucket.
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == '__main__':
    # This is example usage and will not be run by the system.
    # Replace with actual values for testing
    # BUCKET = os.environ.get("S3_BUCKET_NAME", "your-s3-bucket-name")
    # KEY = "my-test-object.txt"
    # LOCAL_FILE = "path/to/local/file.txt"
    # with open(LOCAL_FILE, "w") as f:
    #     f.write("This is a test file content.")
    # upload_object(BUCKET, KEY, LOCAL_FILE)
    pass
