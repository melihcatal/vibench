from database_client import get_table


def fetch_document(table_name, document_id):
    table = get_table(table_name)
    response = table.get_item(Key={"id": document_id})
    return response.get("Item")
