import firebase_admin
from firebase_admin import auth

from identity_client import get_identity_config
from identity_models import normalize_email


def password_reset(payload, config=None):
    cfg = get_identity_config(config)
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": cfg["project_id"]})
    user = auth.get_user_by_email(normalize_email(payload["email"]), app=app)
    link = auth.generate_password_reset_link(user.email, app=app)
    return {"reset_link": link}
