class FetchSecretPayload:
    def __init__(self, secret_id, version='latest', key_field=None):
        self.secret_id = secret_id
        self.version = version
        self.key_field = key_field


class RotateSecretPayload:
    def __init__(self, secret_id, version):
        self.secret_id = secret_id
        self.version = version