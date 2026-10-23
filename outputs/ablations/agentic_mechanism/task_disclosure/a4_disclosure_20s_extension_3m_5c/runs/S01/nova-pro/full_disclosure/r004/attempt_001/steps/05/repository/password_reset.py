import firebase_admin
from firebase_admin import auth

def start_password_reset(email):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    try:
        auth.generate_password_reset_link(email)
        print(f'Password reset link sent to {email}')
    except Exception as e:
        print(f'Error sending password reset link: {e}')

if __name__ == '__main__':\n    email = 'user@example.com'
    start_password_reset(email)