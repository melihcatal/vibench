import os
from identity_client import IdentityClient
from identity_models import UserCredentials

def email_password_login(email, password):
    client = IdentityClient(api_key=os.environ.get("FIREBASE_API_KEY"))
    credentials = UserCredentials(email=email, password=password)
    auth_tokens = client.sign_in_with_email_password(credentials)
    return {
        "id_token": auth_tokens.id_token,
        "refresh_token": auth_tokens.refresh_token,
        "expires_in": auth_tokens.expires_in,
        "user_id": auth_tokens.local_id
    }
