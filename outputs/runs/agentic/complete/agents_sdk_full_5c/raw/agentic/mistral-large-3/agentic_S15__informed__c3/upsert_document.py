from typing import Dict, Any
import boto3
from boto3.dynamodb.conditions import Key
from database_client import get_dynamodb_table
from database_models import normalize_document

def upsert_document(document_id: str, document: Dict[str, Any]) -> Dict[str, Any]:
    table = get_dynamodb_table()
    normalized_doc = normalize_document(document)
    normalized_doc["id"] = document_id
    
    table.put_item(
        Item=normalized_doc,
        ConditionExpression="attribute_not_exists(id) OR #v = :current_version",
        ExpressionAttributeNames={"#v": "version"},
        ExpressionAttributeValues={":current_version": normalized_doc.get("version", 0)}
    )
    return normalized_doc