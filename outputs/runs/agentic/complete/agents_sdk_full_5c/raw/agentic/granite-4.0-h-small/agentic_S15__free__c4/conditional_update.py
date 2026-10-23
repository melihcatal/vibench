# [SAME-SCENARIO] conditional_update.py
from database_client import NoSQLClient

def conditional_update(doc_id, update_payload, condition_expression, expression_attribute_names, expression_attribute_values):
    """Apply a conditional or version‑aware update to a stored document.

    Args:
        doc_id (str): Primary identifier of the document.
        update_payload (dict): Attributes to set or modify.
        condition_expression (str): DynamoDB ConditionExpression (e.g., "attribute_exists (version)").
        expression_attribute_names (dict): Map of #N substitutes for attribute names.
        expression_attribute_values (dict): Map of :V substitutes for attribute values.
    """
    client = NoSQLClient()
    client.update_item(
        TableName=client.table_name,
        Key={'id': {'S': doc_id}},
        UpdateExpression=update_payload['UpdateExpression'],
        ConditionExpression=condition_expression,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=expression_attribute_values
    )
    print(f"Conditional update attempted for document {doc_id}.")