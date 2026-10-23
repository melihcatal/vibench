import datetime
import json
from database_client import get_dynamodb_resource
from database_models import Document

def upsert_document(table_name: str, document: Document) -> dict:
    """
    Upserts a JSON document into DynamoDB by its primary identifier.
    If 'version' is provided, it attempts a conditional update (optimistic locking).
    """
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)

    current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    item = document.model_dump(exclude_unset=True)
    item["updated_at"] = current_time

    if "created_at" not in item:
        item["created_at"] = current_time

    if document.version is not None:
        # Conditional update for optimistic locking
        # Increment version on update
        item["version"] = document.version + 1
        try:
            response = table.put_item(
                Item=item,
                ConditionExpression="attribute_exists(id) AND version = :current_version",
                ExpressionAttributeValues={":current_version": document.version}
            )
        except Exception as e:
            if "ConditionalCheckFailedException" in str(e):
                raise ValueError(f"Document with id {document.id} has been modified by another process.")
            raise
    else:
        # Simple put (create or overwrite without version check)
        if "version" not in item:
            item["version"] = 1 # Initialize version for new documents
        response = table.put_item(Item=item)

    return response
