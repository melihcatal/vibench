import boto3

from identity_models import build_auth_request, build_forgot_password_request, build_sign_up_request, load_config, parse_tokens


def get_cognito_client(config=None):
    cfg = load_config(config)
    return boto3.client("cognito-idp", region_name=cfg["region"]), cfg


def sign_up(payload, config=None):
    client, cfg = get_cognito_client(config)
    response = client.sign_up(**build_sign_up_request(payload, cfg))
    return {"user_id": response["UserSub"]}


def sign_in(payload, config=None):
    client, cfg = get_cognito_client(config)
    response = client.initiate_auth(**build_auth_request(payload, cfg, "USER_PASSWORD_AUTH"))
    return parse_tokens(response)


def refresh_auth(payload, config=None):
    client, cfg = get_cognito_client(config)
    response = client.initiate_auth(**build_auth_request(payload, cfg, "REFRESH_TOKEN_AUTH"))
    return parse_tokens(response)


def start_password_reset(payload, config=None):
    client, cfg = get_cognito_client(config)
    client.forgot_password(**build_forgot_password_request(payload, cfg))
    return {"status": "reset_started", "email": payload["email"]}
