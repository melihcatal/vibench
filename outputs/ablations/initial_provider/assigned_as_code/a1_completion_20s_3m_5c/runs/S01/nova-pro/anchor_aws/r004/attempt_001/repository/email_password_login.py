import firebase_admin
from firebase_admin import auth

def email_password_login(email, password, config=None):
    config = config or {}
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    user = auth.get_user_by_email(email)
    token = auth.create_custom_token(user.uid)
    return {'id_token': token.decode('utf-8')}