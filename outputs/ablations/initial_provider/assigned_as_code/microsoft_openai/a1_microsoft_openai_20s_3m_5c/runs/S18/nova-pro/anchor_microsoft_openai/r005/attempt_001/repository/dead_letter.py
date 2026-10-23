import boto3


def dead_letter(message, config=None):
    config = config or {}
    sqs = boto3.client('sqs', region_name=config['region'])
    dead_letter_queue_url = config['dead_letter_queue_url']
    response = sqs.send_message(
        QueueUrl=dead_letter_queue_url,
        MessageBody=json.dumps(message),
        MessageAttributes={
            'FailedProcessing': {
                'StringValue': 'True',
                'DataType': 'String'
            }
        }
    )
    return response['MessageId']