import firebase_admin
from firebase_admin import auth

from identity_client import load_identity_config, normalized_payload
from identity_models import parse_tokens


def email_password_login(payload, config=None):
    config = load_identity_config(config)
    payload = normalized_payload(payload)
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config.project_id})
    user = auth.get_user_by_email(payload["email"], app=app)
    token = auth.create_custom_token(user.uid, app=app)
    return parse_tokens({"access_token": token.decode("utf-8") if hasattr(token, "decode") else token, "refresh_token": user.uid, "expires_in": 3600})
