from database_client import get_db_table


def fetch_document(document_id: str):
    table = get_db_table()

    response = table.get_item(Key={"documentId": document_id})
    item = response.get("Item")
    return item
