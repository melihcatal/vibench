def normalize_secret_payload(payload):
    return {'secret_id': payload['secret_id'], 'key_field': payload.get('key_field', None)}


def normalize_secret_response(response):
    return {'secret_value': response['payload']['data'].decode('utf-8')}