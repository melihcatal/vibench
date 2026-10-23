from identity_client import cognito_client
from identity_models import extract_token_bundle, normalize_email, secret_hash


def email_password_login(payload, config=None):
    client, loaded = cognito_client(config)
    username = normalize_email(payload["email"])
    request = {
        "AuthFlow": "USER_PASSWORD_AUTH",
        "ClientId": loaded["client_id"],
        "AuthParameters": {"USERNAME": username, "PASSWORD": payload["password"]},
    }
    hash_value = secret_hash(loaded.get("client_secret"), loaded["client_id"], username)
    if hash_value:
        request["AuthParameters"]["SECRET_HASH"] = hash_value
    response = client.initiate_auth(**request)
    return extract_token_bundle(response["AuthenticationResult"])
