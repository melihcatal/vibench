from typing import Dict

class IdentityRequest:
    def __init__(self, scopes: list):
        self.scopes = scopes

class IdentityResponse:
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

class IdentityNormalization:
    @staticmethod
    def normalize_profile(profile: Dict) -> Dict:
        normalized_profile = {
            'id': profile.get('id'),
            'name': profile.get('name'),
            'email': profile.get('email'),
            'picture': profile.get('picture')
        }
        return normalized_profile

if __name__ == '__main__':
    pass