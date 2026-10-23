import firebase_admin
from firebase_admin import auth

from identity_client import get_firebase_app
from identity_models import normalize_email_password_payload


def password_reset(payload, config=None):
    payload = normalize_email_password_payload(payload)
    app = get_firebase_app(config)
    user = auth.get_user_by_email(payload["email"], app=app)
    link = auth.generate_password_reset_link(payload["email"], app=app)
    return {"user_id": user.uid, "reset_link": link}
