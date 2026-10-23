class SecretRequest:
    def __init__(self, project_id, secret_id):
        self.project_id = project_id
        self.secret_id = secret_id

class SecretResponse:
    def __init__(self, data):
        self.data = data

def normalize_secret_response(response):
    return SecretResponse(response)