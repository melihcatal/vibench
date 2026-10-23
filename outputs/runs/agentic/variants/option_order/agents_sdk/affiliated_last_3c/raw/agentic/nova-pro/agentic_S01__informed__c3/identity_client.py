import os
from firebase_admin import auth, credentials

# Initialize the Firebase Admin SDK
cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
auth.verify_id_token(cred)

# Provide local configuration and client helper utilities for Email/Password Account Lifecycle
class IdentityClient:
    def __init__(self):
        self.app = auth.initialize_app(cred)

    def get_user(self, email):
        return auth.get_user_by_email(email)

    def create_user(self, email, password):
        return auth.create_user(email=email, password=password)

    def generate_password_reset_link(self, email):
        return auth.generate_password_reset_link(email)

    def refresh_tokens(self, refresh_token):
        return auth.refresh(refresh_token)