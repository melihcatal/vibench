import json
import os
import sys

import boto3


def publish_event(topic_arn: str, event: dict) -> str:
    sns = boto3.client("sns")
    response = sns.publish(TopicArn=topic_arn, Message=json.dumps(event), MessageStructure="string")
    return response["MessageId"]


def main() -> None:
    topic_arn = os.environ["AWS_SNS_TOPIC_ARN"]
    payload = json.loads(sys.stdin.read() or "{}")
    message_id = publish_event(topic_arn, payload)
    print(message_id)


if __name__ == "__main__":
    main()
