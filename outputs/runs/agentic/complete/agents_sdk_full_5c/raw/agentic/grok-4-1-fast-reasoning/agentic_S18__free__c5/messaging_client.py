import os
from typing import Dict

def get_messaging_config() -&gt; Dict[str, str]:
    return {
        'project_id': os.getenv('GOOGLE_CLOUD_PROJECT'),
        'topic': os.getenv('PUBSUB_TOPIC', 'events-topic'),
        'subscription': os.getenv('PUBSUB_SUBSCRIPTION', 'events-sub'),
        'dl_topic': os.getenv('PUBSUB_DL_TOPIC', 'dead-letter-topic'),
    }