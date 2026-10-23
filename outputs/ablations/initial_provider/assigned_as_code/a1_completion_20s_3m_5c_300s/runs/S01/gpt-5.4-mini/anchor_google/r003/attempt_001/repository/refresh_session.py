import firebase_admin
from firebase_admin import auth

from identity_client import load_identity_config


def refresh_session(payload, config=None):
    config = load_identity_config(config)
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config.project_id})
    decoded = auth.verify_id_token(payload["refresh_token"], app=app, check_revoked=False)
    return {"access_token": auth.create_custom_token(decoded["uid"], app=app).decode("utf-8") if hasattr(auth.create_custom_token(decoded["uid"], app=app), "decode") else auth.create_custom_token(decoded["uid"], app=app), "expires_in": 3600}
