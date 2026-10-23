import firebase_admin
from firebase_admin import auth

firebase_admin.initialize_app()

def start_password_reset(email):
    action_code_settings = auth.ActionCodeSettings(
        url='https://yourapp.com/resetpassword?email={email}',
        handle_code_in_app=True)
    auth.generate_password_reset_link(email, action_code_settings)