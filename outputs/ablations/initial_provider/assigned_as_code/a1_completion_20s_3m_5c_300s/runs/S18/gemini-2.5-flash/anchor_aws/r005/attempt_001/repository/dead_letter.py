import json

from messaging_client import get_sns_client


def dead_letter_event(payload, config=None):
    config = config or {}
    sns_client = get_sns_client(config.get("region"))
    response = sns_client.publish(
        TopicArn=config["dead_letter_topic_arn"],
        Message=json.dumps(payload["event"]),
        MessageAttributes={
            "reason": {
                "DataType": "String",
                "StringValue": payload.get("reason", "Unknown error")
            }
        }
    )
    return {"message_id": response["MessageId"], "status": "dead_lettered"}
