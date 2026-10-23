import boto3

def summarize_message_processing_results(topic_arn, message_id):
    sns_client = boto3.client('sns')
    response = sns_client.get_message_attributes(
        TopicArn=topic_arn,
        MessageId=message_id
    )
    attributes = response['MessageAttributes']
    summary = {
        'message_id': message_id,
        'attributes': attributes
    }
    return summary