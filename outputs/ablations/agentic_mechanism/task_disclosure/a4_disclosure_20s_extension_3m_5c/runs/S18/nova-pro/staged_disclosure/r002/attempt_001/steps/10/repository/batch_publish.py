import boto3

def batch_publish(queue_url, messages):
    sqs = boto3.client('sqs')
    entries = []
    for message in messages:
        entries.append({
            'Id': message['Id'],
            'MessageBody': message['Body'],
            'MessageAttributes': message.get('Attributes', {})
        })
    response = sqs.send_message_batch(
        QueueUrl=queue_url,
        Entries=entries
    )
    return response

if __name__ == '__main__':
    queue_url = 'https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue'
    messages = [
        {
            'Id': '1',
            'Body': 'Hello, World!',
            'Attributes': {
                'Title': {'StringValue': 'Test', 'DataType': 'String'}
            }
        },
        {
            'Id': '2',
            'Body': 'Hello again!',
            'Attributes': {
                'Title': {'StringValue': 'Test', 'DataType': 'String'}
            }
        }
    ]
    response = batch_publish(queue_url, messages)
    print(response)