import boto3

def archive_document(bucket_name: str, file_path: str, object_name: str):
    """
    Archives a document (snapshot or attachment) in AWS S3 managed object storage.

    Args:
        bucket_name (str): The name of the S3 bucket.
        file_path (str): The path to the file to upload.
        object_name (str): The S3 object name (key).
    """
    s3 = boto3.client('s3')
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error archiving document: {e}")

