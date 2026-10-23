import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from messaging_client import get_sns_client, require_config
from messaging_models import normalize_payload, normalize_attributes, make_message_record


def publish_event(payload: Any, topic_arn: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cfg = require_config()
    client = get_sns_client()
    message = normalize_payload(payload)
    attrs = normalize_attributes(attributes)
    response = client.publish(
        TopicArn=topic_arn or cfg["topic_arn"],
        Message=json.dumps(message, ensure_ascii=False),
        MessageAttributes=attrs,
    )
    return make_message_record(
        provider="aws_sns",
        action="publish",
        message_id=response.get("MessageId"),
        status="sent",
        details=response,
    )
