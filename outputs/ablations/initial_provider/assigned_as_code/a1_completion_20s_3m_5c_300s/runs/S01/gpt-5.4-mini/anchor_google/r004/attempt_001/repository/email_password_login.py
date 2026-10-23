from firebase_admin import auth

from identity_client import build_firebase_app
from identity_models import build_account_payload


def email_password_login(payload, config=None):
    app = build_firebase_app(config)
    data = build_account_payload(payload)
    user = auth.get_user_by_email(data["email"], app=app)
    token = auth.create_custom_token(user.uid, app=app)
    return {"user_id": user.uid, "custom_token": token.decode("utf-8") if hasattr(token, "decode") else token}
