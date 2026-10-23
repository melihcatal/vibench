import firebase_admin
from firebase_admin import auth


def password_reset(email, config=None):
    config = config or {}
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    action_code_settings = auth.ActionCodeSettings(
        url='https://www.example.com/resetPassword?email={email}',
        handle_code_in_display_name=True
    )
    auth.generate_password_reset_link(email, action_code_settings, app=app)