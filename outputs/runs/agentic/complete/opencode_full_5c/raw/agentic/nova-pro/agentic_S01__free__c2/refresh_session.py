from firebase_admin import auth, credentials


def refresh_session(id_token):
    new_token = auth.refresh(id_token)
    return new_token
