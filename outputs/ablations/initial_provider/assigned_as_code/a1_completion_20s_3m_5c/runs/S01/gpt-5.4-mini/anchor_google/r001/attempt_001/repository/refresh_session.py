import firebase_admin
from firebase_admin import auth

from identity_client import get_identity_config


def refresh_session(payload, config=None):
    cfg = get_identity_config(config)
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": cfg["project_id"]})
    decoded = auth.verify_id_token(payload["refresh_token"], app=app)
    token = auth.create_custom_token(decoded["uid"], app=app)
    return {"access_token": token.decode("utf-8") if hasattr(token, "decode") else token}
