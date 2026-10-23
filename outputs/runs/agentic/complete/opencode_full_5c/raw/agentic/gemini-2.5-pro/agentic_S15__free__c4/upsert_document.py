import boto3
from decimal import Decimal
import json

from database_client import get_db_table


def upsert_document(document: dict):
    table = get_db_table()
    # DynamoDB doesn't accept floats, convert them to Decimals
    item_decimal = json.loads(json.dumps(document), parse_float=Decimal)
    response = table.put_item(Item=item_decimal)
    return response
