from google.cloud import storage

def normalize_payload(payload):
    """Normalizes the payload for storage operations."""
    return {
        'object_name': payload['object_name'],
        'data': payload['data'],
        'content_type': payload.get('content_type', 'application/octet-stream')
    }

def normalize_response(response):
    """Normalizes the response from storage operations."""
    return {'object_name': response['object_name']}