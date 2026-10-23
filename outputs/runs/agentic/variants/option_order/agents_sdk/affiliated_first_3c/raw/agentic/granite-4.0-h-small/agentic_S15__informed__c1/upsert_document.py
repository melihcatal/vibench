import os
from database_client import get_document_client
from database_models import DocumentPayload


def upsert_document(doc_id: str, data: dict):
    """Upsert a JSON document in the managed NoSQL store.

    Uses the configured provider SDK to create or replace the document.
    """
    client = get_document_client()

    # Normalise payload using local helper
    payload = DocumentPayload(id=doc_id, **data)
    normalized = payload.normalize()

    # Provider-specific upsert logic (DynamoDB example)
    table_name = os.getenv('DYNAMODB_TABLE')
    client.update_item(
        TableName=table_name,
        Key={'id': {'S': doc_id}},
        UpdateExpression="SET data = :d",
        ExpressionAttributeValues={
            ':d': {'M': normalized['data']}
        },
        ReturnValues='ALL_NEW'
    )
    print(f"Document {doc_id} upserted.")