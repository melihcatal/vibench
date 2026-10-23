from database_client import get_dynamodb_table
from database_models import Documents
from boto3.dynamodb.conditions import Attr
from typing import List, Dict, Any

def query_documents(field_name: str, field_value: Any) -> List[Dict[str, Any]]:
    table = get_dynamodb_table()
    response = table.scan(
        FilterExpression=Attr(field_name).eq(field_value)
    )
    return response['Items']