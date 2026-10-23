import firebase_admin
from firebase_admin import credentials, auth

def sign_in_with_email_and_password(email, password):
    if not firebase_admin._apps:
        cred = credentials.Certificate('path/to/serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
    try:
        user = auth.get_user_by_email(email)
        user = auth.sign_in_with_email_and_password(email, password)
        return user.id_token, user.refresh_token
    except Exception as e:
        return str(e)

# Example usage:
# id_token, refresh_token = sign_in_with_email_and_password('user@example.com', 'password123')