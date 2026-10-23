import firebase_admin
from firebase_admin import auth

def register_user(email, password):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    user = auth.create_user(email=email, password=password)
    return user.uid

if __name__ == "__main__":
    email = "user@example.com"
    password = "strongPassword123"
    user_id = register_user(email, password)
    print(f'Successfully registered user with UID: {user_id}')
