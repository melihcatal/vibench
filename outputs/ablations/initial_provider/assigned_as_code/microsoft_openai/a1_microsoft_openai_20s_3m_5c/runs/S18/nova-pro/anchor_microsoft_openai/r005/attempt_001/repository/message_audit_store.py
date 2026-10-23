import boto3


def persist_message_audit(message, config=None):
    config = config or {}
    dynamodb = boto3.resource('dynamodb', region_name=config['region'])
    table = dynamodb.Table(config['table_name'])
    table.put_item(Item=message)
    return message['message_id']