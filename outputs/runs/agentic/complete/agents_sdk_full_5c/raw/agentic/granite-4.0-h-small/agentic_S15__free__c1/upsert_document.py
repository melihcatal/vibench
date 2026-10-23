import os
from database_client import NoSQLClient
from database_models import Document

def upsert_document(primary_id: str, document: dict) -> None:
    """Insert or replace a JSON document in the managed NoSQL store.

    Uses Amazon DynamoDB as the concrete managed NoSQL document store.
    The table name is defined in the environment variable DYNAMODB_TABLE.
    """
    client = NoSQLClient()
    # Ensure the document has the primary key field
    document.setdefault('id', primary_id)
    # Convert to the model format expected by the client helper
    payload = Document(**document).to_dict()
    client.put_item(TableName=os.getenv('DYNAMODB_TABLE'), Item=payload)
