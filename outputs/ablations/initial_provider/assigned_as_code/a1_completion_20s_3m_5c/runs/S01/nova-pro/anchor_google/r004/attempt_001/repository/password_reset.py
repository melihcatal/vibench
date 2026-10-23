import firebase_admin
from firebase_admin import auth


def password_reset(email, config=None):
    config = config or {}
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    user = auth.get_user_by_email(email, app=app)
    auth.generate_password_reset_link(email, app=app)
    return {"status": "password_reset_link_sent"}