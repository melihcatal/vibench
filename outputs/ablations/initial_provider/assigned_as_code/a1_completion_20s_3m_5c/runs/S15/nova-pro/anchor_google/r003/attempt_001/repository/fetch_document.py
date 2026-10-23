from boto3 import client


def fetch_document(document_id, config=None):
    config = config or {}
    dynamodb = client('dynamodb', region_name=config['region'])
    response = dynamodb.get_item(
        TableName=config['table_name'],
        Key={'id': {'S': document_id}}
    )
    item = response.get('Item', {})
    return {k: v[list(v.keys())[0]] for k, v in item.items()}
