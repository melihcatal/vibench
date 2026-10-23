from identity_client import app_client_id, cognito_client
from identity_models import EmailPasswordLogin, response_payload, token_bundle


def email_password_login(email: str, password: str):
    req = EmailPasswordLogin(email=email, password=password).normalized()
    client = cognito_client()
    result = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        ClientId=app_client_id(),
        AuthParameters={"USERNAME": req["email"], "PASSWORD": req["password"]},
    )
    auth = result.get("AuthenticationResult", {})
    return response_payload(
        "Amazon Cognito User Pools",
        "email_password_login",
        token_bundle(
            auth.get("AccessToken"), auth.get("RefreshToken"), auth.get("IdToken")
        ),
    )
