from database_client import get_dynamodb_client
from database_models import normalize_response


def conditional_update(
    document_id: str, update_expression: str, expression_attribute_values: Dict
):
    client = get_dynamodb_client()
    response = client.update_item(
        TableName=DYNAMODB_TABLE_NAME,
        Key={document_id: {"S": document_id}},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
    )
    return normalize_response(response)
