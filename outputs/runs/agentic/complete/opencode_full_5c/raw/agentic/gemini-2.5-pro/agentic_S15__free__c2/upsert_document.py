from database_client import get_db_client, get_table_name
from database_models import Document
from decimal import Decimal
import json


def upsert_document(document: Document):
    dynamodb = get_db_client()
    table_name = get_table_name()
    table = dynamodb.Table(table_name)

    document_dict = json.loads(document.model_dump_json(), parse_float=Decimal)

    response = table.put_item(Item=document_dict)
    return response
