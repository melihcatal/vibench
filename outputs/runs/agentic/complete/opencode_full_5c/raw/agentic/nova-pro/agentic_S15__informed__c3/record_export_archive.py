import boto3


def record_export_archive(bucket_name, file_name, file_content):
    s3_client = boto3.client("s3")
    try:
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)
        print(f"File {file_name} uploaded successfully.")
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None
