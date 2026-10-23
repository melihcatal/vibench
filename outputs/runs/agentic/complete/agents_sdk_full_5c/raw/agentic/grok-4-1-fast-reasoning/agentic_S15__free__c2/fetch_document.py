from database_client import get_dynamodb_table
from database_models import parse_fetched_item, Document
from typing import Optional

def fetch_document(identifier: str) -> Optional[Document]:
    table = get_dynamodb_table()
    response = table.get_item(Key={'id': identifier})
    return parse_fetched_item(response.get('Item'))