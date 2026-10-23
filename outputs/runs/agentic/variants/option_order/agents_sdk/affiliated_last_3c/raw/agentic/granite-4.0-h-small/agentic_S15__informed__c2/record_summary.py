import os
from database_client import get_dynamodb_client

def summarize_documents(table_name, partition_key, partition_value, filter_expr=None):
    """Retrieve documents and produce a concise textual summary.

    Uses the managed DynamoDB store for data retrieval.
    """
    client = get_dynamodb_client()
    KeyConditionExpr = f"#{partition_key} = :val"
    expression_values = {
        ":val": {'S': str(partition_value)}
    }
    if filter_expr:
        filter_parts = []
        for f in filter_expr:
            name = f['name']
            value = f['value']
            op = f['operator'].upper()
            if op == 'EQ':
                filter_parts.append(f"#{name} = :{name}")
                expression_values[f":{name}"] = {'S': str(value)}
        filter_expr_str = " AND ".join(filter_parts) if filter_parts else None

    query_kwargs = {
        'TableName': table_name,
        'KeyConditionExpression': KeyConditionExpr,
    }
    if filter_expr_str:
        query_kwargs['FilterExpression'] = filter_expr_str
    query_kwargs['ExpressionAttributeNames'] = {"#" + partition_key: partition_key}
    query_kwargs['ExpressionAttributeValues'] = expression_values

    response = client.query(**query_kwargs)
    items = response.get('Items', [])
    summaries = []
    for item in items:
        # Use the normalized data from DocumentResponse
        doc = DocumentResponse(item).data
        summary = f"ID: {doc.get('id', 'N/A')}, Name: {doc.get('name', 'N/A')}, Status: {doc.get('status', 'N/A')}"
        summaries.append(summary)
    return summaries
