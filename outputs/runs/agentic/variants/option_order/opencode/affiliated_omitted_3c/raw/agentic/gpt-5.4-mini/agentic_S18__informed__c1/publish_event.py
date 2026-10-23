import json
import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from messaging_client import get_sns_client, get_topic_arn
from messaging_models import normalize_message_payload, build_publish_response


def publish_event(payload: Dict[str, Any], subject: Optional[str] = None) -> Dict[str, Any]:
    client = get_sns_client()
    topic_arn = get_topic_arn()
    normalized = normalize_message_payload(payload)
    message = json.dumps(normalized, separators=(",", ":"), sort_keys=True)
    kwargs = {"TopicArn": topic_arn, "Message": message}
    if subject:
        kwargs["Subject"] = subject[:100]
    try:
        response = client.publish(**kwargs)
    except (BotoCoreError, ClientError) as exc:
        return build_publish_response(False, error=str(exc))
    return build_publish_response(True, message_id=response.get("MessageId"), provider="aws-sns")
