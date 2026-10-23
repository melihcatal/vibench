from typing import Dict

class AuthResponse:
    def __init__(self, auth_code: str, auth_code_response: Dict):
        self.auth_code = auth_code
        self.auth_code_response = auth_code_response

class TokenResponse:
    def __init__(self, access_token: str, refresh_token: str, expires_in: int):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in

if __name__ == '__main__':
    pass