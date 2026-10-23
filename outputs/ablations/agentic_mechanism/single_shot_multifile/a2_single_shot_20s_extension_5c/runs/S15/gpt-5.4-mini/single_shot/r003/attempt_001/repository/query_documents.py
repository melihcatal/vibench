import boto3
from botocore.exceptions import ClientError
from database_client import get_table_name, get_dynamodb_resource, get_query_index_name, get_partition_key_name
from database_models import QueryDocumentsRequest, query_result


def handler(event, context=None):
    request = QueryDocumentsRequest.from_event(event)
    table = get_dynamodb_resource().Table(get_table_name())
    partition_key_name = get_partition_key_name()
    index_name = get_query_index_name()
    try:
        if index_name:
            response = table.query(
                IndexName=index_name,
                KeyConditionExpression=boto3.dynamodb.conditions.Key(partition_key_name).eq(request.field_value),
            )
        else:
            response = table.scan(
                FilterExpression=boto3.dynamodb.conditions.Attr(request.field_name).eq(request.field_value)
            )
        return query_result(response.get('Items', []))
    except ClientError as exc:
        raise RuntimeError(str(exc))
