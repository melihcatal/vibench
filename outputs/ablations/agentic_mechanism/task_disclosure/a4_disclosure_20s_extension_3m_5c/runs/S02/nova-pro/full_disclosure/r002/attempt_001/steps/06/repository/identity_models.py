from bedrock import Bedrock

class FederatedLoginRequest:
    def __init__(self, client_id, redirect_uri, scope):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope

    def to_dict(self):
        return {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope
        }


class FederatedLoginResponse:
    def __init__(self, access_token, token_type, expires_in):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in

    @staticmethod
    def from_dict(data):
        return FederatedLoginResponse(
            data['access_token'],
            data['token_type'],
            data['expires_in']
        )


def normalize_federated_login_response(response):
    bedrock_client = Bedrock()
    normalized_response = bedrock_client.normalize(response)
    return FederatedLoginResponse.from_dict(normalized_response)