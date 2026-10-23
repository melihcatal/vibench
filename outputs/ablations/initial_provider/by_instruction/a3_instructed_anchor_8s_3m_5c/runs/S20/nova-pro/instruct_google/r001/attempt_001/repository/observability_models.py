from typing import Dict

def normalize_log_event(event: Dict):
    return {
        'severity': event.get('severity', 'DEFAULT'),
        'message': event.get('message', ''),
        'component': event.get('component', ''),
        'operation': event.get('operation', '')
    }