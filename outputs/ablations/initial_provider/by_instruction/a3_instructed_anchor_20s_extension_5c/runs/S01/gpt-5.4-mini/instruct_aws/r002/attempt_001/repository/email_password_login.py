from identity_client import cognito_idp_client, identity_client_id
from identity_models import EmailPasswordRequest, normalize_email, tokens_from_cognito_response


def login_user(request: EmailPasswordRequest):
    client = cognito_idp_client()
    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": normalize_email(request.email), "PASSWORD": request.password},
        ClientId=identity_client_id(),
    )
    return tokens_from_cognito_response(response.get("AuthenticationResult", {}))
