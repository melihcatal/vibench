class AuthResponse:
    def __init__(self, response):
        self.access_token = response.get('AuthenticationResult', {}).get('AccessToken')
        self.id_token = response.get('AuthenticationResult', {}).get('IdToken')
        self.refresh_token = response.get('AuthenticationResult', {}).get('RefreshToken')