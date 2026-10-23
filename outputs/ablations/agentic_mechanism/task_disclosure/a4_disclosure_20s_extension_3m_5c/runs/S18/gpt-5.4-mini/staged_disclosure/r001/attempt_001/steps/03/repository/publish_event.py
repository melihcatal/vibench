import json
import os
from typing import Any, Dict, Optional

import boto3


def publish_event(event: Dict[str, Any], topic_arn: Optional[str] = None) -> str:
    sns = boto3.client("sns")
    arn = topic_arn or os.environ["AWS_SNS_TOPIC_ARN"]
    response = sns.publish(TopicArn=arn, Message=json.dumps(event), MessageStructure="string")
    return response["MessageId"]


def main() -> None:
    event = json.loads(os.environ.get("EVENT_JSON", "{}"))
    publish_event(event)


if __name__ == "__main__":
    main()
