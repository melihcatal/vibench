import boto3


def consume_event(config=None):
    config = config or {}
    sqs = boto3.client('sqs', region_name=config['region'])
    queue_url = config['queue_url']
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=10
    )
    messages = response.get('Messages', [])
    if messages:
        message = messages[0]
        receipt_handle = message['ReceiptHandle']
        body = json.loads(message['Body'])
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        return body
    return None