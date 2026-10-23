from identity_client import cognito_idp_client, identity_client_id
from identity_models import AuthTokens, tokens_from_cognito_response


def refresh_session(tokens: AuthTokens):
    client = cognito_idp_client()
    response = client.initiate_auth(
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={"REFRESH_TOKEN": tokens.refresh_token},
        ClientId=identity_client_id(),
    )
    return tokens_from_cognito_response(response.get("AuthenticationResult", {}))
