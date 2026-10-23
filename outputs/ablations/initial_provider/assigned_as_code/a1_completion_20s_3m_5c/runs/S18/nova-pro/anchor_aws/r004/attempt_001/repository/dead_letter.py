import boto3

from messaging_client import get_sns_client


def dead_letter(payload, config=None):
    config = config or {}
    client = get_sns_client()
    response = client.publish(TopicArn=config['dead_letter_topic_arn'], Message=json.dumps(payload))
    return {'message_id': response['MessageId']}