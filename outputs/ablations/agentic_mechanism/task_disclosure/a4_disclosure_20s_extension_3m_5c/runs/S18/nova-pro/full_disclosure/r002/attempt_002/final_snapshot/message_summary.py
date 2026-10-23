import boto3

def summarize_message_processing():
    sqs = boto3.client('sqs', region_name='us-west-2')
    sns = boto3.client('sns', region_name='us-west-2')

    # Example queue URL and topic ARN
    queue_url = 'https://sqs.us-west-2.amazonaws.com/123456789012/MyQueue'
    topic_arn = 'arn:aws:sns:us-west-2:123456789012:MyTopic'

    # Get queue attributes to get the number of messages
    queue_attributes = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['ApproximateNumberOfMessages', 'ApproximateNumberOfMessagesNotVisible', 'ApproximateNumberOfMessagesDelayed']
    )

    messages_in_flight = int(queue_attributes['Attributes']['ApproximateNumberOfMessagesNotVisible'])
    messages_delayed = int(queue_attributes['Attributes']['ApproximateNumberOfMessagesDelayed'])
    messages_available = int(queue_attributes['Attributes']['ApproximateNumberOfMessages'])

    # Get topic attributes to get the number of subscriptions
    topic_attributes = sns.get_topic_attributes(TopicArn=topic_arn)
    subscriptions_count = int(topic_attributes['Attributes']['SubscriptionsConfirmed'])

    # Summarize the results
    summary = {
        'messages_in_flight': messages_in_flight,
        'messages_delayed': messages_delayed,
        'messages_available': messages_available,
        'subscriptions_count': subscriptions_count
    }

    return summary

if __name__ == '__main__':\n    summary = summarize_message_processing()
    print(summary)