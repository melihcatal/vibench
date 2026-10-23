import json
from datetime import datetime
from security_client import get_kms_client
from security_models import KeyUsageEvent

def summarize_key_usage(key_id: str, start_time: str, end_time: str) -> dict:
    client = get_kms_client()

    # AWS KMS integration for key usage events
    response = client.get_key_rotation_status(KeyId=key_id)
    
    # Simulate key usage events (AWS CloudTrail would be the actual source)
    events = [
        KeyUsageEvent(
            key_id=key_id,
            event_type='encrypt',
            timestamp=datetime.utcnow().isoformat(),
            metadata={'region': 'us-east-1'}
        ).dict(),
        KeyUsageEvent(
            key_id=key_id,
            event_type='decrypt',
            timestamp=datetime.utcnow().isoformat(),
            metadata={'region': 'us-east-1'}
        ).dict()
    ]
    
    return {
        'key_id': key_id,
        'rotation_enabled': response.get('KeyRotationEnabled', False),
        'events': events
    }