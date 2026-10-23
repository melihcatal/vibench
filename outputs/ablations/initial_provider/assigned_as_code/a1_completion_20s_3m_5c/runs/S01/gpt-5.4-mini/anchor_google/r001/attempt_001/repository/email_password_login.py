import firebase_admin
from firebase_admin import auth

from identity_client import get_identity_config
from identity_models import IdentityRequest, IdentityResponse


def email_password_login(payload, config=None):
    cfg = get_identity_config(config)
    req = IdentityRequest(payload)
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": cfg["project_id"]})
    user = auth.get_user_by_email(req.email(), app=app)
    token = auth.create_custom_token(user.uid, app=app)
    return IdentityResponse({"user_id": user.uid, "token": token.decode("utf-8") if hasattr(token, "decode") else token}).as_dict()
