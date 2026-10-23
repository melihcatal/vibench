from firebase_admin import auth


def password_reset(email):
    action_code_settings = auth.ActionCodeSettings(
        url="https://yourapp.com/reset_password", handle_code_in_app=True
    )
    auth.generate_password_reset_link(email, action_code_settings)
