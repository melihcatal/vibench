import os
import json
from datetime import datetime
import requests
from identity_models import AuthCodeExchangeResult

def store_audit_record(event: Dict[str, Any]):
    """
    Persist a single federated-login audit event to IBM Cloudant (managed NoSQL document store).
    The function expects Cloudant URL and API key to be set in environment variables:
        - CLOUDANT_URL   (e.g., https://my-account.cloudant.com)
        - CLOUDANT_APIKEY (Cloudant API key with writer permissions)
    The event dict must contain at least:
        - event_id: str (unique identifier)
        - timestamp: ISO8601 string or datetime
        - user_id: str
        - action: str (e.g., 'oauth_code_exchange')
        - success: bool
        - details: dict (optional)
    """
    CLOUDANT_URL = os.getenv('CLOUDANT_URL')
    CLOUDANT_APIKEY = os.getenv('CLOUDANT_APIKEY')
    if not CLOUDANT_URL or not CLOUDANT_APIKEY:
        raise RuntimeError('Cloudant credentials missing (CLOUDANT_URL, CLOUDANT_APIKEY)')

    # Normalize timestamp to ISO8601 string if needed
    event['timestamp'] = event['timestamp'].isoformat() if isinstance(event['timestamp'], datetime) else str(event['timestamp'])

    # Optional: snapshot the AuthCodeExchangeResult if present
    if 'token_data' in event and isinstance(event['token_data'], dict):
        # Persist a reduced payload (remove sensitive tokens for storage)
        token_snapshot = {
            'access_token_md5': 'md5*' + hashlib.md5(event['token_data'].get('access_token', '').encode()).hexdigest(),
            'id_token_md5': 'md5*' + hashlib.md5(event['token_data'].get('id_token', '').encode()).hexdigest(),
            'expires_in': event['token_data'].get('expires_in')
        }
        event['token_snapshot'] = token_snapshot

    # Use the 'events' database (create on first write if missing)
    db_name = 'events'
    db_url = f'{CLOUDANT_URL}/{db_name}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {CLOUDANT_APIKEY}'
    }
    # Cloudant expects the _id field to be set; use event_id or generate one
    event_id = event.get('event_id') or str(datetime.utcnow().isoformat())
    event['_id'] = event_id

    resp = requests.post(db_url, headers=headers, json=event, timeout=10)
    if resp.status_code not in (201, 200):
        raise RuntimeError(f'Failed to store audit event: {resp.status_code} {resp.text}')
    print(f'Stored audit event {event_id} successfully.')

if __name__ == '__main__':
    # Demo event creation
    demo_event = {
        'event_id': 'demo-1234',
        'timestamp': datetime.utcnow(),
        'user_id': 'user_demo',
        'action': 'oauth_code_exchange',
        'success': True,
        'details': {
            'access_token': 'tok123',
            'id_token': 'id123',
            'expires_in': 3600
        }
    }
    store_audit_record(demo_event)