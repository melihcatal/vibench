import base64
import hashlib
import hmac


def _secret_hash(email, client_id, client_secret):
    digest = hmac.new(client_secret.encode(), (email + client_id).encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def load_config(config=None):
    config = config or {}
    return {
        "region": config.get("region"),
        "client_id": config["client_id"],
        "client_secret": config.get("client_secret"),
        "table_name": config.get("table_name"),
        "locale": config.get("locale", "en"),
    }


def normalize_email(email):
    return email.strip().lower()


def cognito_secret_hash(email, client_id, client_secret):
    return _secret_hash(email, client_id, client_secret) if client_secret else None


def build_sign_up_request(payload, config):
    email = normalize_email(payload["email"])
    request = {"ClientId": config["client_id"], "Username": email, "Password": payload["password"], "UserAttributes": [{"Name": "email", "Value": email}]}
    secret_hash = cognito_secret_hash(email, config["client_id"], config.get("client_secret"))
    if secret_hash:
        request["SecretHash"] = secret_hash
    return request


def build_auth_request(payload, config, auth_flow):
    email = normalize_email(payload["email"])
    request = {"AuthFlow": auth_flow, "ClientId": config["client_id"], "AuthParameters": {"USERNAME": email}}
    if "password" in payload:
        request["AuthParameters"]["PASSWORD"] = payload["password"]
    secret_hash = cognito_secret_hash(email, config["client_id"], config.get("client_secret"))
    if secret_hash:
        request["AuthParameters"]["SECRET_HASH"] = secret_hash
    if "refresh_token" in payload:
        request["AuthParameters"]["REFRESH_TOKEN"] = payload["refresh_token"]
    return request


def build_forgot_password_request(payload, config):
    email = normalize_email(payload["email"])
    request = {"ClientId": config["client_id"], "Username": email}
    secret_hash = cognito_secret_hash(email, config["client_id"], config.get("client_secret"))
    if secret_hash:
        request["SecretHash"] = secret_hash
    return request


def parse_tokens(response):
    auth = response.get("AuthenticationResult", {})
    return {"access_token": auth.get("AccessToken"), "id_token": auth.get("IdToken"), "refresh_token": auth.get("RefreshToken"), "expires_in": auth.get("ExpiresIn")}
