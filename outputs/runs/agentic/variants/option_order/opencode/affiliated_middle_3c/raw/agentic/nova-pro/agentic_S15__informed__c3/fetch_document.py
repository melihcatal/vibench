from database_client import get_dynamodb_client
from database_models import normalize_response


def fetch_document(document_id: str):
    client = get_dynamodb_client()
    response = client.get_item(
        TableName=DYNAMODB_TABLE_NAME, Key={document_id: {"S": document_id}}
    )
    return normalize_response(response)
