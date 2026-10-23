import firebase_admin
from firebase_admin import auth

def password_reset(email):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    action_code_settings = auth.ActionCodeSettings(
        url='https://yourapp.com/resetpassword?email={email}',
        handle_code_in_app=True
    )
    auth.generate_password_reset_link(email, action_code_settings)