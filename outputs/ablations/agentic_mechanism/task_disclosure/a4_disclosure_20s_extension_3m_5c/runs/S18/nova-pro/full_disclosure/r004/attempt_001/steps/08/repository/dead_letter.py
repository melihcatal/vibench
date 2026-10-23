import boto3

def send_to_dead_letter(message, topic_arn):
    sns_client = boto3.client('sns')
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )
    return response

if __name__ == '__main__'):
    failed_message = 'This is a failed message'
    dead_letter_topic_arn = 'arn:aws:sns:us-east-1:123456789012:DeadLetterTopic'
    response = send_to_dead_letter(failed_message, dead_letter_topic_arn)
    print(response)