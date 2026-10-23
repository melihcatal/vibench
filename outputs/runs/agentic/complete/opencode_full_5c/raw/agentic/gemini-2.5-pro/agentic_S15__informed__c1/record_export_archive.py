import os
import json
import boto3
from botocore.exceptions import ClientError
from database_models import Document


def record_export_archive(record: Document, bucket_name: str):
    """
    Exports a document to a JSON file and archives it in Amazon S3.

    :param record: The document record to archive.
    :param bucket_name: The name of the S3 bucket.
    :return: True if the upload was successful, False otherwise.
    """
    s3_client = boto3.client("s3")

    document_id = record.get("document_id")
    if not document_id:
        raise ValueError("Record must have a 'document_id'")

    file_name = f"{document_id}.json"
    object_name = f"archive/{file_name}"

    try:
        # Serialize the document to a JSON string
        file_content = json.dumps(record, indent=4)

        # Upload the JSON string as a file to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=file_content.encode("utf-8"),
            ContentType="application/json",
        )

    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return False
    return True
