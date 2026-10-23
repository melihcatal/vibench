import os
from firebase_admin import auth


def refresh_session(refresh_token):
    try:
        new_tokens = auth.refresh_custom_token(refresh_token)
        return new_tokens
    except Exception as e:
        print(f"Error refreshing session: {e}")
        return None
