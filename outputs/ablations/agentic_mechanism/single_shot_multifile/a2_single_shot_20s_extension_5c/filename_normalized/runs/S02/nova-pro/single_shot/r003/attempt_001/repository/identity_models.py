class OAuth2Response:
    def __init__(self, data):
        self.access_token = data.get('access_token')
        self.refresh_token = data.get('refresh_token')
        self.expires_in = data.get('expires_in')
        self.token_type = data.get('token_type')
        self.id_token = data.get('id_token')

class UserInfo:
    def __init__(self, data):
        self.sub = data.get('sub')
        self.name = data.get('name')
        self.email = data.get('email')