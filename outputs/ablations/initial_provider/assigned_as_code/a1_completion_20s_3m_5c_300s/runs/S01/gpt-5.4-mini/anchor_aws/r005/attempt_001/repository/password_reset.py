from identity_client import cognito_client
from identity_models import normalize_email, secret_hash


def password_reset(payload, config=None):
    client, loaded = cognito_client(config)
    username = normalize_email(payload["email"])
    request = {"ClientId": loaded["client_id"], "Username": username}
    hash_value = secret_hash(loaded.get("client_secret"), loaded["client_id"], username)
    if hash_value:
        request["SecretHash"] = hash_value
    response = client.forgot_password(**request)
    return {"delivery": response["CodeDeliveryDetails"]}
