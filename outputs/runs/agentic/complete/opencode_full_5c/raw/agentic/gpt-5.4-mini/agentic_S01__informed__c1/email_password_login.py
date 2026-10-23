from identity_client import auth0_json_post, build_password_grant, parse_token_set


def email_password_login(email: str, password: str) -> dict:
    token_set = parse_token_set(auth0_json_post("/oauth/token", build_password_grant(email, password)))
    return token_set.__dict__
