import firebase_admin
from firebase_admin import auth

from identity_client import get_firebase_app
from identity_models import normalize_email_password_payload


def email_password_login(payload, config=None):
    payload = normalize_email_password_payload(payload)
    app = get_firebase_app(config)
    user = auth.get_user_by_email(payload["email"], app=app)
    token = auth.create_custom_token(user.uid, app=app)
    return {"user_id": user.uid, "id_token": token.decode("utf-8") if isinstance(token, bytes) else token}
