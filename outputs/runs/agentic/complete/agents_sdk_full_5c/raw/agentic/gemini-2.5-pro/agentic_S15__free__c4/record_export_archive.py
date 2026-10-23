import os
import json
import boto3
from botocore.exceptions import ClientError

def archive_document(document_id: str, document_data: dict):
    """
    Archives a document snapshot as a JSON file in Amazon S3.

    :param document_id: The ID of the document, used as the S3 object key.
    :param document_data: The document content to archive.
    :return: True if upload was successful, False otherwise.
    """
    bucket_name = os.environ.get("S3_ARCHIVE_BUCKET")
    if not bucket_name:
        raise ValueError("S3_ARCHIVE_BUCKET environment variable not set.")
    
    s3_client = boto3.client("s3")
    object_key = f"archive/{document_id}.json"
    
    try:
        # Serialize the dictionary to a JSON string
        json_body = json.dumps(document_data, indent=2)
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json_body,
            ContentType='application/json'
        )
        print(f"Successfully archived document {document_id} to s3://{bucket_name}/{object_key}")
        return True
    except ClientError as e:
        print(f"Failed to upload to S3: {e}")
        return False
    except TypeError as e:
        print(f"Failed to serialize document data to JSON: {e}")
        return False
