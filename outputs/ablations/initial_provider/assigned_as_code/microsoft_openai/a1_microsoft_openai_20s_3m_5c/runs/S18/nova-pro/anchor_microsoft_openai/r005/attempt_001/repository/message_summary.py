import boto3


def summarize_message_processing(messages, config=None):
    config = config or {}
    dynamodb = boto3.resource('dynamodb', region_name=config['region'])
    table = dynamodb.Table(config['table_name'])
    summary = {
        'total_messages': len(messages),
        'successful_messages': sum(1 for message in messages if message['status'] == 'SUCCESS'),
        'failed_messages': sum(1 for message in messages if message['status'] == 'FAILURE')
    }
    table.put_item(Item=summary)
    return summary