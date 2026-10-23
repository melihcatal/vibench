def normalize_secret_payload(payload):
    return {'secret_id': payload.get('secret_id'), 'key_field': payload.get('key_field')}

def normalize_secret_response(response):
    return {'api_key': response.get('api_key')}