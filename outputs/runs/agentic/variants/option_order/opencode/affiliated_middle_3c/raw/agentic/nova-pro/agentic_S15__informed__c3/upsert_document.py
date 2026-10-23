from database_client import get_dynamodb_client
from database_models import normalize_response


def upsert_document(document_id: str, document: Dict):
    client = get_dynamodb_client()
    response = client.put_item(
        TableName=DYNAMODB_TABLE_NAME, Item={document_id: {"S": json.dumps(document)}}
    )
    return normalize_response(response)
