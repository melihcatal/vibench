from identity_client import cognito_client
from identity_models import extract_token_bundle, normalize_email, secret_hash


def refresh_session(payload, config=None):
    client, loaded = cognito_client(config)
    username = normalize_email(payload["email"])
    request = {
        "AuthFlow": "REFRESH_TOKEN_AUTH",
        "ClientId": loaded["client_id"],
        "AuthParameters": {"REFRESH_TOKEN": payload["refresh_token"], "USERNAME": username},
    }
    hash_value = secret_hash(loaded.get("client_secret"), loaded["client_id"], username)
    if hash_value:
        request["AuthParameters"]["SECRET_HASH"] = hash_value
    response = client.initiate_auth(**request)
    return extract_token_bundle(response["AuthenticationResult"])
