import firebase_admin
from firebase_admin import auth

from identity_client import get_firebase_app


def refresh_session(payload, config=None):
    payload = payload or {}
    app = get_firebase_app(config)
    decoded = auth.verify_id_token(payload["refresh_token"], app=app, check_revoked=False)
    user = auth.get_user(decoded["uid"], app=app)
    token = auth.create_custom_token(user.uid, app=app)
    return {"user_id": user.uid, "access_token": token.decode("utf-8") if isinstance(token, bytes) else token}
