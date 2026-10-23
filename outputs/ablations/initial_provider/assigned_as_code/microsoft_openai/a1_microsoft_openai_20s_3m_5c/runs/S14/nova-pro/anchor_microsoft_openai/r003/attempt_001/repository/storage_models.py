from azure.storage.blob import ContentSettings


def normalize_upload_payload(payload):
    normalized_payload = {
        'object_name': payload['object_name'],
        'data': payload['data'],
        'content_type': payload.get('content_type', 'application/octet-stream'),
        'content_settings': ContentSettings(content_type=payload.get('content_type', 'application/octet-stream'))
    }
    return normalized_payload