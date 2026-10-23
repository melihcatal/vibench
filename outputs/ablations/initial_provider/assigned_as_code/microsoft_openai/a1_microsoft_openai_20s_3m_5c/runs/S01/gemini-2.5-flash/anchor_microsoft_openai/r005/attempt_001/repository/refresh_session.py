from identity_client import AzureADB2CClient
from identity_models import TokenRefreshRequest, TokenRefreshResponse

def refresh_session(request: TokenRefreshRequest):
    client = AzureADB2CClient()
    response_data = client.refresh_token(request.refresh_token)
    return TokenRefreshResponse(
        access_token=response_data["access_token"],
        id_token=response_data.get("id_token"),
        expires_in=response_data["expires_in"],
        token_type=response_data["token_type"]
    )
