from database_client import get_dynamodb_resource
from database_models import Document, QueryCondition
from typing import List, Dict, Any
import boto3.dynamodb.conditions as conditions

def query_documents(table_name: str, query_conditions: List[QueryCondition]) -> List[Document]:
    """
    Queries documents by a field value or partition-style key from DynamoDB.
    Assumes the table has a primary key 'id' and potentially other indexes.
    For complex queries, consider using a GSI.
    This example focuses on simple queries using `query` or `scan`.

    Note: DynamoDB `query` operations require specifying a partition key and optionally a sort key.
    If querying on non-key attributes, a `scan` is performed, which can be inefficient for large tables.
    For efficient queries on non-key attributes, consider setting up Global Secondary Indexes (GSIs).
    """
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(table_name)

    # For simplicity, if the query includes the 'id' field, we'll try to use query.
    # Otherwise, we'll use scan, which is less efficient but more flexible for non-indexed fields.
    filter_expression = None
    key_condition_expression = None
    expression_attribute_values = {}

    # A basic implementation for a single query condition.
    # For multiple conditions, more complex logic for combining `and` / `or` would be needed.
    # And for `query` vs `scan`, we need to check if the condition matches a key.

    # Example of how to structure conditions for a scan operation
    for i, condition in enumerate(query_conditions):
        attr_name = condition.field_name
        attr_value = condition.field_value
        op = condition.operator

        placeholder_value = f":val{i}"

        if filter_expression is None:
            filter_expression = conditions.Attr(attr_name)
        else:
            filter_expression = filter_expression & conditions.Attr(attr_name)

        if op == '=':
            filter_expression = filter_expression.eq(attr_value)
        elif op == '<':
            filter_expression = filter_expression.lt(attr_value)
        elif op == '>':
            filter_expression = filter_expression.gt(attr_value)
        elif op == '<=':
            filter_expression = filter_expression.le(attr_value)
        elif op == '>=':
            filter_expression = filter_expression.ge(attr_value)
        elif op == 'begins_with':
            filter_expression = filter_expression.begins_with(attr_value)
        # Add more operators as needed

        expression_attribute_values[placeholder_value] = attr_value

    if filter_expression is not None:
        response = table.scan(
            FilterExpression=filter_expression
        )
    else:
        response = table.scan()

    documents = [Document(**item) for item in response.get('Items', [])]
    return documents
