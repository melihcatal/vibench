from identity_client import cognito_idp_client, identity_client_id, identity_user_pool_id
from identity_models import EmailPasswordRequest, normalize_email, normalize_locale


def register_user(request: EmailPasswordRequest):
    client = cognito_idp_client()
    email = normalize_email(request.email)
    locale = normalize_locale(request.locale)
    client.sign_up(
        ClientId=identity_client_id(),
        Username=email,
        Password=request.password,
        UserAttributes=[
            {"Name": "email", "Value": email},
            {"Name": "locale", "Value": locale},
            {"Name": "custom:source", "Value": "email_password_lifecycle"},
        ],
    )
    client.admin_update_user_attributes(
        UserPoolId=identity_user_pool_id(),
        Username=email,
        UserAttributes=[{"Name": "email_verified", "Value": "true"}],
    )
    return {"email": email, "status": "registered", "locale": locale}
