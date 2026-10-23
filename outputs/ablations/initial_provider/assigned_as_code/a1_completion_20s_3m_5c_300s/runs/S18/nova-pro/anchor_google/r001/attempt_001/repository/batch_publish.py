from messaging_client import get_sns_client

def batch_publish(payloads, topic_arn):
    client = get_sns_client()
    messages = [{"Data": json.dumps(payload), "Id": str(i)} for i, payload in enumerate(payloads)]
    response = client.publish_batch(PublishBatchRequestEntries=messages, TopicArn=topic_arn)
    return response['Successful']