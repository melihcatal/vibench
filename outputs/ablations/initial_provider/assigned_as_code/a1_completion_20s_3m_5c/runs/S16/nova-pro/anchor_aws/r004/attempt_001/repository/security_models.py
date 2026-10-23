class SecretRequest:
    def __init__(self, secret_id, key_field=None):
        self.secret_id = secret_id
        self.key_field = key_field


class SecretResponse:
    def __init__(self, secret_value):
        self.secret_value = secret_value