from identity_client import cognito_idp_client, load_identity_config
from identity_models import RefreshRequest, to_payload


def refresh_session(refresh_token: str):
    config = load_identity_config()
    client = cognito_idp_client()
    payload = to_payload(RefreshRequest(refresh_token=refresh_token))
    response = client.initiate_auth(
        ClientId=config.client_id,
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={"REFRESH_TOKEN": payload["refresh_token"]},
    )
    result = response.get("AuthenticationResult", {})
    return {
        "access_token": result.get("AccessToken"),
        "id_token": result.get("IdToken"),
        "expires_in": result.get("ExpiresIn"),
        "token_type": result.get("TokenType"),
    }
