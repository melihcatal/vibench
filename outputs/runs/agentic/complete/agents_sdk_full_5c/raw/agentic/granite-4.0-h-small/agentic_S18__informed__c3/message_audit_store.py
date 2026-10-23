import json
import os

# Load service endpoint and credentials from environment
ENDPOINT = os.getenv('MESSAGE_AUDIT_STORE_ENDPOINT')
API_KEY = os.getenv('MESSAGE_AUDIT_STORE_API_KEY')
if not ENDPOINT or not API_KEY:
    raise RuntimeError('Set MESSAGE_AUDIT_STORE_ENDPOINT and MESSAGE_AUDIT_STORE_API_KEY')

def persist(record):
    """Persist a processed message record to a managed NoSQL store.",
    record (dict): Dictionary containing fields like id, topic, payload, status, etc.",
    """
    import requests
    url = f'{ENDPOINT}/messages'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    try:
        resp = requests.post(url, json=record, headers=headers, timeout=10)
        resp.raise_for_status()
        print(f'Record persisted, status {resp.status_code}')
    except Exception as e:
        print(f'Failed to store record: {e}')

if __name__ == '__main__':
    # Example usage
    example_record = {
        'id': 'evt_123',
        'topic': 'my_topic',
        'payload': {'msg': 'test'},
        'status': 'processed'
    }
    persist(example_record)
