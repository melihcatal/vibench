import os
from firebase_admin import auth

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"


def refresh_session(refresh_token):
    try:
        decoded_token = auth.verify_id_token(refresh_token)
        uid = decoded_token["uid"]
        new_token = auth.create_custom_token(uid)
        return new_token
    except Exception as e:
        return str(e)
