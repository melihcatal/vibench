from messaging_client import get_sns_client
from messaging_models import Message

def dead_letter(message, dead_letter_topic_arn):
    client = get_sns_client()
    client.publish(TopicArn=dead_letter_topic_arn, Message=json.dumps(message.payload))