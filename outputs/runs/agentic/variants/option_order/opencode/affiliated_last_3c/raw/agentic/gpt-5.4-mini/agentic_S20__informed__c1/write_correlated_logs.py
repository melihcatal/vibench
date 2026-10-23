from observability_client import write_log_event
from observability_models import normalize_event


def main() -> list:
    request_id = 'req-abc-789'
    events = [
        normalize_event('request received', 'orders-api', 'info', request_id, {'step': 'ingress'}),
        normalize_event('validated order', 'orders-api', 'info', request_id, {'step': 'validation'}),
        normalize_event('persisted order', 'orders-api', 'info', request_id, {'step': 'storage'}),
    ]
    return [write_log_event(event) for event in events]
