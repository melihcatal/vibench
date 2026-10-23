def normalize_message(payload):
    if isinstance(payload, dict):
        return payload
    return {'event': payload}


def build_message_record(message_id=None, payload=None, status=None, details=None):
    return {
        'message_id': message_id,
        'payload': payload,
        'status': status,
        'details': details or {},
    }


def summarize_outcome(processed=0, failed=0, dead_lettered=0):
    return {
        'processed': processed,
        'failed': failed,
        'dead_lettered': dead_lettered,
    }
