def normalize_payload(payload):
    return {'secret_id': payload['secret_id'], 'version': payload.get('version', 'latest'), 'key_field': payload.get('key_field')}


def parse_response(response):
    return response.payload.data.decode('utf-8')