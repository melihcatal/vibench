from database_client import get_db_table


def fetch_document(document_id: str):
    table = get_db_table()
    response = table.get_item(Key={"id": document_id})
    return response.get("Item")
