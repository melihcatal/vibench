import os
from firebase_admin import auth, credentials

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/serviceAccountKey.json'
cred = credentials.Certificate('path/to/serviceAccountKey.json')
app = firebase_admin.initialize_app(cred)

def password_reset(email):
    action_code_settings = auth.ActionCodeSettings(
        url='https://yourapp.com/reset_password?email={email}',
        handle_code_in_app=True)
    auth.generate_password_reset_link(email, action_code_settings)
    return 'Password reset link sent to email'