def normalize_email(value):
    return (value or "").strip().lower()


def normalize_locale(value):
    value = (value or "").strip()
    return value.replace("_", "-") if value else "en-US"


def build_cognito_username(payload):
    return normalize_email(payload.get("email") or payload.get("username"))


def build_user_attributes(email, extras=None):
    attributes = [{"Name": "email", "Value": normalize_email(email)}]
    for key, value in (extras or {}).items():
        if value is not None:
            attributes.append({"Name": key, "Value": str(value)})
    return attributes


def extract_tokens(response):
    auth = response.get("AuthenticationResult", response)
    return {
        "access_token": auth.get("AccessToken"),
        "id_token": auth.get("IdToken"),
        "refresh_token": auth.get("RefreshToken"),
        "expires_in": auth.get("ExpiresIn"),
        "token_type": auth.get("TokenType"),
    }
