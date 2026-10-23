from typing import Any, Dict, Union


class FederatedLoginRequest:
    def __init__(self, provider: str, redirect_uri: str, state: str):
        self.provider = provider
        self.redirect_uri = redirect_uri
        self.state = state

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FederatedLoginRequest":
        return FederatedLoginRequest(
            provider=data["provider"],
            redirect_uri=data["redirect_uri"],
            state=data["state"],
        )


class FederatedLoginResponse:
    def __init__(self, access_token: str, id_token: str, expires_in: int):
        self.access_token = access_token
        self.id_token = id_token
        self.expires_in = expires_in

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FederatedLoginResponse":
        return FederatedLoginResponse(
            access_token=data["access_token"],
            id_token=data["id_token"],
            expires_in=data["expires_in"],
        )


def normalize_federated_login_response(response: Dict[str, Any]) -> FederatedLoginResponse:
    return FederatedLoginResponse.from_dict(response)