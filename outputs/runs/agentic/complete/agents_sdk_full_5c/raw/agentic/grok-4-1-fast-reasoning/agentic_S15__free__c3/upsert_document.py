from database_client import get_dynamodb_table

def upsert_document(document_id: str, document_data: dict, version: int = 0):
    table = get_dynamodb_table()
    item = {
        'id': document_id,
        'data': document_data,
        'version': version
    }
    table.put_item(Item=item)
