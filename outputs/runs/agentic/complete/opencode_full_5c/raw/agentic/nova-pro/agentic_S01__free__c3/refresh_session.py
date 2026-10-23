import firebase_admin
from firebase_admin import auth


def refresh_session(id_token):
    new_tokens = auth.refresh_id_token(id_token)
    return new_tokens
