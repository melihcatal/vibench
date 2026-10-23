from observability_client import write_log_event
from observability_models import normalize_event


def main() -> dict:
    event = normalize_event(
        message='structured log event',
        service='checkout-api',
        status='info',
        extra={'event_type': 'audit', 'user_id': 'u-12345', 'correlation_id': 'req-001'}
    )
    return write_log_event(event)
