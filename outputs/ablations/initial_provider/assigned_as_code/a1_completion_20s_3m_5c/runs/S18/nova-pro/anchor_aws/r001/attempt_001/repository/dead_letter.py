import boto3

def dead_letter(message, config=None):
    config = config or {}
    sqs = boto3.client('sqs', region_name=config.get('region'))
    dead_letter_queue_url = config['dead_letter_queue_url']
    response = sqs.send_message(QueueUrl=dead_letter_queue_url, MessageBody=message['Body'])
    return {'message_id': response['MessageId']}