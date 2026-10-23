from database_client import get_db_table

def fetch_document_by_id(document_id: str):
    """
    Fetches a single document by its primary key from AWS DynamoDB.

    Provider: AWS DynamoDB
    """
    table = get_db_table()
    response = table.get_item(
        Key={
            'document_id': document_id
        }
    )
    return response.get('Item')
