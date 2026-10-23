class OAuthResponse:
    def __init__(self, data):
        self.access_token = data.get('access_token')
        self.id_token = data.get('id_token')
        self.refresh_token = data.get('refresh_token')
        self.expires_in = data.get('expires_in')


class ProfileClaims:
    def __init__(self, data):
        self.user_id = data.get('id')
        self.display_name = data.get('displayName')
        self.email = data.get('mail')