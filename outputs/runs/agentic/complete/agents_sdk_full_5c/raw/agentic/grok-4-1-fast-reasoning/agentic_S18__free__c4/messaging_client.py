import os
from typing import Optional

_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
_TOPIC_ID = os.getenv('PUBSUB_TOPIC_ID', 'events-topic')
_SUBSCRIPTION_ID = os.getenv('PUBSUB_SUBSCRIPTION_ID', 'events-sub')
_DEAD_LETTER_TOPIC_ID = os.getenv('DEAD_LETTER_TOPIC_ID', 'events-dead-letter')

def get_project_id() -> str:
    if not _PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")
    return _PROJECT_ID

def topic_path(topic_id: Optional[str] = None) -> str:
    tid = topic_id or _TOPIC_ID
    return f"projects/{get_project_id()}/topics/{tid}"

def subscription_path(sub_id: Optional[str] = None) -> str:
    sid = sub_id or _SUBSCRIPTION_ID
    return f"projects/{get_project_id()}/subscriptions/{sid}"

def dead_letter_topic_path() -> str:
    return topic_path(_DEAD_LETTER_TOPIC_ID)