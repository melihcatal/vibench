from typing import Any, Dict
import boto3


def expense_record_store(record: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.resource('dynamodb')
    table = client.Table('expense_records')
    table.put_item(Item=record)
    return {'stored': True, 'provider': 'dynamodb'}
