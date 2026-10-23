from identity_client import build_authorize_url, sign_state, get_env


def start_oauth_login(state: str, secret: str, scope: str = "openid profile email") -> dict:
    signed = sign_state(secret, state)
    return {"authorization_url": build_authorize_url(state=signed, scope=scope), "state": signed, "provider": "AWS Cognito"}


if __name__ == "__main__":
    raise SystemExit(0)
