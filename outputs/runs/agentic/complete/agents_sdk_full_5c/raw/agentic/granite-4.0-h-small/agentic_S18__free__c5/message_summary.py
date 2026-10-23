import os
import json
from messaging_client import PubSubClient
from messaging_models import EventMessage

def summarize_processing(results):
    """Summarize processing outcomes (success, dead-letter, error)."""
    # Assume results is a list of dicts with keys: 'message_id', 'status', 'error'
    summary = {'success': 0, 'dead_letter': 0, 'errors': 0}
    for r in results:
        if r['status'] == 'success':
            summary['success'] += 1
        elif r['status'] == 'dead_letter':
            summary['dead_letter'] += 1
        else:
            summary['errors'] += 1
    # Persist summary to a monitoring topic (e.g., summary-pubsub)
    project_id = os.getenv('PUBSUB_PROJECT_ID')
    if not project_id:
        raise RuntimeError('PUBSUB_PROJECT_ID not set for summary publishing')
    client = PubSubClient(project_id=project_id)
    topic_id = os.getenv('SUMMARY_TOPIC_ID', 'summary-pubsub')
    payload = {'summary': summary, 'timestamp': datetime.utcnow().isoformat()}
    client.publish(topic_id, payload)
    print('Summary published')
