import os
from firebase_admin import auth, credentials

cred = credentials.Certificate("path/to/serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)

def password_reset(email):
    try:
        action_code_settings = auth.ActionCodeSettings(
            url="https://yourapp.com/resetpassword?email=" + email,
            handle_code_in_app=True)
        auth.generate_password_reset_link(email, action_code_settings)
        return True
    except Exception as e:
        raise e