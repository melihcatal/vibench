import os
from database_client import get_dynamodb_client

def query_documents(table_name, partition_key, partition_value, filters=None):
    """Query DynamoDB documents by a partition key value and optional filters.

    Args:
        table_name (str): DynamoDB table name.
        partition_key (str): Attribute name of the partition (hash) key.
        partition_value (str): Value to match for the partition key.
        filters (list, optional): List of attribute condition expressions (e.g., [{'name': 'age', 'value': 30, 'operator': 'EQ'}]).

    Returns:
        list: Matching documents.
    """
    client = get_dynamodb_client()
    KeyConditionExpr = f"#{partition_key} = :val"
    expression_values = {
        ":val": {'S': str(partition_value)}
    }
    if filters:
        condition_parts = []
        for f in filters:
            name = f['name']
            value = f['value']
            operator = f['operator'].upper()
            if operator == 'EQ':
                condition_parts.append(f"#{name} = :{name}")
                expression_values[f":{name}"] = {'S': str(value)}
            elif operator == 'GT':
                condition_parts.append(f"#{name} > :{name}")
                expression_values[f":{name}"] = {'N': str(value)}
            # Add more operators as needed
        filter_expr = " AND ".join(condition_parts)
    else:
        filter_expr = None

    query_kwargs = {
        'TableName': table_name,
        'KeyConditionExpression': KeyConditionExpr,
    }
    if filter_expr:
        query_kwargs['FilterExpression'] = filter_expr
    query_kwargs['ExpressionAttributeNames'] = {"#" + partition_key: partition_key}
    query_kwargs['ExpressionAttributeValues'] = expression_values

    response = client.query(**query_kwargs)
    items = response.get('Items', [])
    return items
