import boto3
from botocore.exceptions import ClientError
from database_client import get_database_client, get_table_name
from database_models import Document
import uuid
import datetime


def upsert_document(document: Document) -> dict:
    """
    Upserts a document into DynamoDB.
    """
    dynamodb = get_database_client()
    table = dynamodb.Table(get_table_name())

    if "document_id" not in document or not document["document_id"]:
        document["document_id"] = str(uuid.uuid4())

    if "created_at" not in document or not document["created_at"]:
        document["created_at"] = datetime.datetime.utcnow().isoformat()

    if "version" not in document:
        document["version"] = 1

    try:
        response = table.put_item(Item=document)
        return {
            "status": "success",
            "document_id": document["document_id"],
            "response": response,
        }
    except ClientError as e:
        return {"status": "error", "message": e.response["Error"]["Message"]}
