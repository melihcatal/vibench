import boto3

def summarize_message_processing_results(topic_arn, message_id):
    sns_client = boto3.client('sns')
    try:
        response = sns_client.get_message_attributes(
            TopicArn=topic_arn,
            MessageId=message_id
        )
        print(f'Message attributes: {response['MessageAttributes']}')
    except Exception as e:
        print(f'Error summarizing message processing results: {e}')

# Example usage
# summarize_message_processing_results('arn:aws:sns:us-east-1:123456789012:MyTopic', 'abcd1234-5678-90ef-ghij-klmnopqrstu')