import os
from firebase_admin import auth, credentials

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/serviceAccountKey.json'
cred = credentials.Certificate('path/to/serviceAccountKey.json')
app = firebase_admin.initialize_app(cred)

def email_password_login(email, password):
    user = auth.get_user_by_email(email)
    custom_token = auth.create_custom_token(user.uid)
    return custom_token