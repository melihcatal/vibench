import os
import json
import boto3
from botocore.exceptions import ClientError

def archive_document_to_s3(document_id: str, document_data: dict):
    """
    Archives a document snapshot as a JSON file in an Amazon S3 bucket.

    Args:
        document_id: The unique ID of the document.
        document_data: The document content to archive.

    Returns:
        True if upload is successful, False otherwise.
    """
    bucket_name = os.environ.get("S3_ARCHIVE_BUCKET")
    if not bucket_name:
        raise ValueError("S3_ARCHIVE_BUCKET environment variable is not set.")

    s3_resource = boto3.resource('s3')
    object_key = f"document-archives/{document_id}/{document_id}.json"

    try:
        s3_object = s3_resource.Object(bucket_name, object_key)
        
        # Convert the document data to a JSON string
        json_string = json.dumps(document_data, indent=2, default=str)

        response = s3_object.put(
            Body=json_string,
            ContentType='application/json'
        )
        
        # Check if the upload was successful
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print(f"Successfully archived document {document_id} to s3://{bucket_name}/{object_key}")
            return True
        else:
            print(f"Failed to archive document {document_id}. Status: {response['ResponseMetadata']['HTTPStatusCode']}")
            return False

    except ClientError as e:
        print(f"An error occurred uploading to S3: {e}")
        return False
