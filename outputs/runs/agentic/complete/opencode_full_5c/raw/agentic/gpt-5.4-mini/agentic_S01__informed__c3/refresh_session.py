from identity_client import app_client_id, cognito_client
from identity_models import response_payload, token_bundle


def refresh_session(refresh_token: str):
    client = cognito_client()
    result = client.initiate_auth(
        AuthFlow="REFRESH_TOKEN_AUTH",
        ClientId=app_client_id(),
        AuthParameters={"REFRESH_TOKEN": refresh_token},
    )
    auth = result.get("AuthenticationResult", {})
    return response_payload(
        "Amazon Cognito User Pools",
        "refresh_session",
        token_bundle(
            auth.get("AccessToken"), auth.get("RefreshToken"), auth.get("IdToken")
        ),
    )
