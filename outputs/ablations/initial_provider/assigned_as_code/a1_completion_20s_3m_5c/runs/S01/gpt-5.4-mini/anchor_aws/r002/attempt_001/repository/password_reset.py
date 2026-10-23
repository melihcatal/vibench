from identity_client import add_secret_hash, create_cognito_client, prepare_username


def password_reset(payload, config=None):
    client, cfg = create_cognito_client(config)
    username = prepare_username(payload)
    request = {"ClientId": cfg["client_id"], "Username": username}
    add_secret_hash(request, cfg, username)
    response = client.forgot_password(**request)
    return {"delivery": response.get("CodeDeliveryDetails", {})}
