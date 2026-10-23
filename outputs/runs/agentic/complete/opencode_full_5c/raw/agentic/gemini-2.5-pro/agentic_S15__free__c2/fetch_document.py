from database_client import get_db_client, get_table_name


def fetch_document(document_id: str):
    dynamodb = get_db_client()
    table_name = get_table_name()
    table = dynamodb.Table(table_name)

    response = table.get_item(Key={"document_id": document_id})
    return response.get("Item")
