import firebase_admin
from firebase_admin import auth


def email_password_login(email, password, config=None):
    config = config or {}
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    user = auth.get_user_by_email(email, app=app)
    custom_token = auth.create_custom_token(user.uid)
    return custom_token.decode('utf-8')