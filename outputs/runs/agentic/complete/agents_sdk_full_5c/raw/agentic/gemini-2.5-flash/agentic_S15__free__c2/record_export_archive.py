import boto3
import os

def archive_document_to_s3(bucket_name: str, object_key: str, file_path: str = None, file_content: bytes = None) -> dict:
    """
    Archives exported document snapshots or attachments to AWS S3 managed object storage.
    Either file_path or file_content must be provided.
    Requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION environment variables.
    """
    s3 = boto3.client('s3', region_name=os.getenv('AWS_REGION'))
    try:
        if file_path:
            with open(file_path, 'rb') as f:
                s3.upload_fileobj(f, bucket_name, object_key)
            print(f"File '{file_path}' uploaded to s3://{bucket_name}/{object_key}")
        elif file_content:
            s3.put_object(Bucket=bucket_name, Key=object_key, Body=file_content)
            print(f"Content uploaded to s3://{bucket_name}/{object_key}")
        else:
            raise ValueError("Either file_path or file_content must be provided.")

        return {"bucket": bucket_name, "key": object_key, "status": "success"}
    except Exception as e:
        print(f"Error archiving document to S3: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires AWS credentials and an S3 bucket)
    # os.environ['AWS_ACCESS_KEY_ID'] = 'YOUR_AWS_ACCESS_KEY_ID' # Replace with your actual key
    # os.environ['AWS_SECRET_ACCESS_KEY'] = 'YOUR_AWS_SECRET_ACCESS_KEY' # Replace with your actual secret
    # os.environ['AWS_REGION'] = 'us-east-1' # Example

    # s3_bucket_name = "your-unique-s3-bucket-name" # Replace with your S3 bucket name
    # s3_object_key = "documents/snapshot_doc123_20231027.json"

    # # Example 1: Uploading a dummy file (create one first for testing)
    # # with open("test_document.json", "w") as f:
    # #     f.write('{"id": "doc123", "title": "Archived Doc"}')
    # # try:
    # #     archive_document_to_s3(s3_bucket_name, "documents/test_document.json", file_path="test_document.json")
    # # except Exception as e:
    # #     print(f"File upload failed: {e}")

    # # Example 2: Uploading content directly
    # content_to_archive = b'{"id": "doc456", "title": "Another Archived Doc", "status": "completed"}'
    # s3_object_key_content = "documents/snapshot_doc456_content.json"
    # try:
    #     archive_document_to_s3(s3_bucket_name, s3_object_key_content, file_content=content_to_archive)
    # except Exception as e:
    #     print(f"Content upload failed: {e}")

    # if not os.getenv('AWS_ACCESS_KEY_ID'):
    #     print("Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables for example usage.")
    # if not os.getenv('AWS_REGION'):
    #     print("Please set AWS_REGION environment variable for example usage.")
