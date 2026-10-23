import firebase_admin
from firebase_admin import auth

def register_user(email, password):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except Exception as e:
        print(f'Error registering user: {e}')
        return None