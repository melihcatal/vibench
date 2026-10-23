import json

from messaging_client import sns_client, load_config
from messaging_models import normalize_message


def batch_publish(payload, config=None):
    config = load_config(config)
    client = sns_client(config)
    messages = payload.get("messages", [])
    results = []
    for index, message in enumerate(messages):
        normalized = normalize_message(message)
        response = client.publish(TopicArn=config["topic_arn"], Message=json.dumps(normalized))
        results.append({"message_id": response.get("MessageId")})
    return {"results": results}
