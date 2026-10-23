import json
from database_client import get_dynamodb_client, get_dynamodb_table_name
from database_models import Document

def upsert_document(document: Document):
    dynamodb = get_dynamodb_client()
    table_name = get_dynamodb_table_name()

    item = {
        'id': {'S': document['id']},
        'content': {'S': json.dumps(document['content'])}
    }

    response = dynamodb.put_item(
        TableName=table_name,
        Item=item
    )
    return response
