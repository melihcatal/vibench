class SecretRequest:
    def __init__(self, vault_url, secret_name):
        self.vault_url = vault_url
        self.secret_name = secret_name

class SecretResponse:
    def __init__(self, value):
        self.value = value