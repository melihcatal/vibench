import boto3

def store_message_audit(message, config=None):
    config = config or {}
    dynamodb = boto3.resource('dynamodb', region_name=config.get('region'))
    table = dynamodb.Table(config['table_name'])
    table.put_item(Item=message)