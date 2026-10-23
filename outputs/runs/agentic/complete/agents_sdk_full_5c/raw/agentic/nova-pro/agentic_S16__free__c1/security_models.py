class SecretRequest:
    def __init__(self, secret_id, version_stage=None):
        self.secret_id = secret_id
        self.version_stage = version_stage

class SecretResponse:
    def __init__(self, secret_string):
        self.secret_string = secret_string