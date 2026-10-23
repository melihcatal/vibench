import firebase_admin
from firebase_admin import auth

from identity_client import load_identity_config, normalized_payload


def password_reset(payload, config=None):
    config = load_identity_config(config)
    payload = normalized_payload(payload)
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config.project_id})
    user = auth.get_user_by_email(payload["email"], app=app)
    link = auth.generate_password_reset_link(payload["email"], app=app)
    return {"user_id": user.uid, "reset_link": link}
