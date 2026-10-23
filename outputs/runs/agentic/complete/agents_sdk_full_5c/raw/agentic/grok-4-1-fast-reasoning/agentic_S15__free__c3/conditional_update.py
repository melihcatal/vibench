from database_client import get_dynamodb_table
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

def conditional_update(document_id: str, new_data: dict, expected_version: int) -> bool:
    table = get_dynamodb_table()
    try:
        table.update_item(
            Key={'id': document_id},
            UpdateExpression='SET data = :data, version = :new_version',
            ConditionExpression=Attr('version').eq(expected_version),
            ExpressionAttributeValues={
                ':data': new_data,
                ':new_version': expected_version + 1
            }
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return False
        raise
