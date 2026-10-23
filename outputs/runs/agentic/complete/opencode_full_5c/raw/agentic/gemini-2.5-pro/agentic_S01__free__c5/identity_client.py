import os
import firebase_admin
from firebase_admin import credentials


def get_firebase_app():
    if not firebase_admin._apps:
        cred_path = os.environ.get("FIREBASE_ADMIN_SDK_CREDENTIALS")
        if cred_path:
            cred = credentials.Certificate(cred_path)
        else:
            # For environments where service account is discovered automatically
            cred = credentials.ApplicationDefault()

        firebase_admin.initialize_app(
            cred,
            {
                "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
            },
        )
    return firebase_admin.get_app()


def get_firebase_api_key():
    return os.environ.get("FIREBASE_API_KEY")


def get_identity_toolkit_url():
    return "https://identitytoolkit.googleapis.com/v1/accounts"


def get_secure_token_url():
    return "https://securetoken.googleapis.com/v1/token"
