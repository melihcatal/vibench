import boto3

def publish_batch(topic_arn, messages):
    sns = boto3.client('sns')
    publish_entries = [{"Id": str(i), "Message": message} for i, message in enumerate(messages)]
    response = sns.publish_batch(TopicArn=topic_arn, PublishBatchRequestEntries=publish_entries)
    return response

if __name__ == '__main__':
    topic_arn = 'arn:aws:sns:REGION:ACCOUNT_ID:TOPIC_NAME'
    messages = ['Message 1', 'Message 2', 'Message 3']
    response = publish_batch(topic_arn, messages)
    print(response)