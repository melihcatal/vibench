import firebase_admin
from firebase_admin import credentials, auth

try:
    cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
except ValueError:
    if not firebase_admin._apps:
        pass

def email_password_login(email: str, password: str) -> dict:
    try:
        user = auth.get_user_by_email(email)
        uid = user.uid
        custom_token = auth.create_custom_token(uid)
        return {
            "custom_token": custom_token.decode('utf-8')
        }
    except Exception as e:
        return {"error": str(e)}
