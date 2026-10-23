import boto3
from botocore.exceptions import ClientError
from database_client import get_table_name, get_dynamodb_resource, get_document_id_name, get_version_attribute_name
from database_models import ConditionalUpdateRequest, conditional_update_result, normalize_update_expression


def handler(event, context=None):
    request = ConditionalUpdateRequest.from_event(event)
    table = get_dynamodb_resource().Table(get_table_name())
    document_id_name = get_document_id_name()
    version_attr = get_version_attribute_name()
    update_expression, expression_names, expression_values = normalize_update_expression(request.updates, version_attr)
    condition_expression = boto3.dynamodb.conditions.Attr(document_id_name).exists()
    if request.expected_version is not None:
        condition_expression = condition_expression & boto3.dynamodb.conditions.Attr(version_attr).eq(request.expected_version)
    try:
        response = table.update_item(
            Key={document_id_name: request.document_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ConditionExpression=condition_expression,
            ReturnValues='ALL_NEW',
        )
        return conditional_update_result(response.get('Attributes', {}))
    except ClientError as exc:
        raise RuntimeError(str(exc))
