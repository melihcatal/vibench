class SecretRequest:
    def __init__(self, secret_id, key_field=None, version=None):
        self.secret_id = secret_id
        self.key_field = key_field
        self.version = version

class SecretResponse:
    def __init__(self, secret_value):
        self.secret_value = secret_value

def normalize_payload(payload):
    return {'secret_id': payload['secret_id'], 'key_field': payload.get('key_field'), 'version': payload.get('version')}