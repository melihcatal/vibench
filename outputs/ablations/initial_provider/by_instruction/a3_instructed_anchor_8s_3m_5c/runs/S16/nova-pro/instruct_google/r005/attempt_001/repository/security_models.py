class SecretRequest:
    def __init__(self, project_id, secret_id, version='latest'):
        self.project_id = project_id
        self.secret_id = secret_id
        self.version = version

class SecretResponse:
    def __init__(self, data):
        self.data = data

def normalize_secret_response(response):
    return SecretResponse(response.payload.data.decode('UTF-8'))