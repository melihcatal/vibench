import boto3

def batch_publish(payloads, config=None):
    config = config or {}
    sns = boto3.client('sns', region_name=config.get('region'))
    topic_arn = config['topic_arn']
    message_ids = []
    for payload in payloads:
        response = sns.publish(TopicArn=topic_arn, Message=json.dumps(payload['event']))
        message_ids.append(response['MessageId'])
    return {'message_ids': message_ids}