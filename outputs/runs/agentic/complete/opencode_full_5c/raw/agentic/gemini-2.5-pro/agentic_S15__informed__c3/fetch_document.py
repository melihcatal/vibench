from database_client import get_db_client, DOCUMENTS_TABLE_NAME


def fetch_document(category: str, document_id: str):
    dynamodb = get_db_client()
    response = dynamodb.get_item(
        TableName=DOCUMENTS_TABLE_NAME,
        Key={"category": {"S": category}, "id": {"S": document_id}},
    )
    return response.get("Item")
