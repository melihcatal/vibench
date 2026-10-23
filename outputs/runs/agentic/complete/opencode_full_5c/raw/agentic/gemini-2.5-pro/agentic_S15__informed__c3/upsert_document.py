from database_client import get_db_client, DOCUMENTS_TABLE_NAME
from database_models import Document


def upsert_document(document: Document):
    dynamodb = get_db_client()

    item = {
        "category": {"S": document["category"]},
        "id": {"S": document["id"]},
        "content": {"S": document["content"]},
        "version": {"N": str(document["version"])},
    }

    response = dynamodb.put_item(TableName=DOCUMENTS_TABLE_NAME, Item=item)
    return response
