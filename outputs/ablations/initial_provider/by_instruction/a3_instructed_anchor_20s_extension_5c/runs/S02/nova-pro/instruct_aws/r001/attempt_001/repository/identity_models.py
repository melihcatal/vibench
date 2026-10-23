class AuthResponse:
    def __init__(self, response):
        self.response = response

    def get_access_token(self):
        return self.response['AuthenticationResult']['AccessToken']

    def get_id_token(self):
        return self.response['AuthenticationResult']['IdToken']

    def get_refresh_token(self):
        return self.response['AuthenticationResult']['RefreshToken']