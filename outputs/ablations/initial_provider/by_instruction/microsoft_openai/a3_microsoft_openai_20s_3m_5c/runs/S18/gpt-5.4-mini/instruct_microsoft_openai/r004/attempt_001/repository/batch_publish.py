import json

from messaging_client import create_client, get_topic_name


def batch_publish(messages):
    with create_client() as client:
        sender = client.get_topic_sender(topic_name=get_topic_name())
        with sender:
            sender.send_messages([json.dumps(message) for message in messages])
    return {"count": len(messages)}
