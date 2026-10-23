import firebase_admin
from firebase_admin import auth


def password_reset(email, config=None):
    config = config or {}
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    auth.generate_password_reset_link(email, app=app)
    return {"message": "Password reset link sent."}
