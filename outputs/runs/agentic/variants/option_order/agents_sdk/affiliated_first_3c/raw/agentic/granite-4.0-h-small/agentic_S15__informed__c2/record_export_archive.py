import os
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def archive_document(collection_name, doc_id, bucket_name, object_key):
    """Archive a document snapshot to Amazon S3.\n    The document is fetched from Cosmos DB, converted to JSON, and stored as an object in S3.\n    """
    # Fetch document from Cosmos DB (reuse fetch_document logic)
    client = boto3.client('cosmosdb', use_ssl=True)
    # Since boto3 does not have native Cosmos DB client, we assume the user has access via DynamoDB resource for illustration
    # Here we use S3 client directly, fetching document from Cosmos via HTTP or another client if needed.
    try:
        # For demo, assume document already fetched and stored in variable 'doc'
        doc = {"id": doc_id, "snapshot": "example"}
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).put_object(Key=object_key, Body=json.dumps(doc))
        print(f"Document {doc_id} archived to S3 bucket {bucket_name} under key {object_key}.")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print("AWS credentials error:", e)
    except Exception as e:
        print("Unexpected error during archiving:", e)

if __name__ == "__main__":
    # Example usage - archive document 'sample-001' into bucket 'my-archive-bucket' with key 'documents/sample-001.json'
    archive_document("mycontainer", "sample-001", "my-archive-bucket", "documents/sample-001.json")
