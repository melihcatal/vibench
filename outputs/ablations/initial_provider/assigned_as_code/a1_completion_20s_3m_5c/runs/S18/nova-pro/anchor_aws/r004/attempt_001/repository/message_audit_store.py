import boto3


def message_audit_store(payload):
    client = boto3.client('dynamodb', region_name=os.getenv('AWS_REGION'))
    client.put_item(TableName='MessageAudit', Item={'message_id': {'S': payload['message_id']}, 'payload': {'S': json.dumps(payload)}})