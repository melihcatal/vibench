class OAuthTokenResponse:
    def __init__(self, access_token, token_type, expires_in, scope):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope

    @classmethod
    def from_dict(cls, data):
        return cls(
            access_token=data.get('access_token'),
            token_type=data.get('token_type'),
            expires_in=data.get('expires_in'),
            scope=data.get('scope'),
        )

class UserProfile:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get('name'),
            id=data.get('id'),
        )