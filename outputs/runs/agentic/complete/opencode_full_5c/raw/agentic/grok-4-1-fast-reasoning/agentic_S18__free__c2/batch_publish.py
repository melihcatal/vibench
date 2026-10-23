import json
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from messaging_client import publish_message, topic_id


def batch_publish(events: List[Dict[str, Any]]) -> List[str]:
    def _publish_one(event: Dict[str, Any]) -> str:
        data = json.dumps(event).encode("utf-8")
        return publish_message(topic_id, data)

    msg_ids = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_event = {
            executor.submit(_publish_one, event): event for event in events
        }
        for future in as_completed(future_to_event):
            msg_ids.append(future.result())
    return msg_ids
