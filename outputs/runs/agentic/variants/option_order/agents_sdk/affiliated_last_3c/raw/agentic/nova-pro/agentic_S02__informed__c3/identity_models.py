class IdentityRequest:
    def __init__(self, scopes):
        self.scopes = scopes

class IdentityResponse:
    def __init__(self, tokens):
        self.tokens = tokens

def normalize_claims(claims):
    return {
        'sub': claims.get('sub'),
        'email': claims.get('email'),
        'name': claims.get('name'),
    }

if __name__ == '__main__':
    request = IdentityRequest(['openid', 'email', 'profile'])
    response = IdentityResponse({'access_token': 'your_access_token'})
    claims = normalize_claims({'sub': 'user_id', 'email': 'user@example.com', 'name': 'User Name'})
    print(request, response, claims