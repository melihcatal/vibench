import os

PROJECT_ID = os.getenv('GCP_PROJECT_ID')
TOPIC_ID = os.getenv('TOPIC_ID', 'events-topic')
SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID', 'events-sub')
DEAD_LETTER_TOPIC_ID = os.getenv('DEAD_LETTER_TOPIC_ID', 'dead-letter-topic')

def topic_path(topic_id: str = TOPIC_ID) -> str:
    return f'projects/{PROJECT_ID}/topics/{topic_id}'

def subscription_path(sub_id: str = SUBSCRIPTION_ID) -> str:
    return f'projects/{PROJECT_ID}/subscriptions/{sub_id}'