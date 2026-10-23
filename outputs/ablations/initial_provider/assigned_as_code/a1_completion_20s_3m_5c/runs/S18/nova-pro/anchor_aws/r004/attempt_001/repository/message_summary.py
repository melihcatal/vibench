from messaging_client import get_sqs_client


def message_summary(queue_name):
    client = get_sqs_client()
    response = client.get_queue_attributes(QueueUrl=client.get_queue_url(QueueName=queue_name)['QueueUrl'], AttributeNames=['ApproximateNumberOfMessages', 'ApproximateNumberOfMessagesNotVisible'])
    return response['Attributes']