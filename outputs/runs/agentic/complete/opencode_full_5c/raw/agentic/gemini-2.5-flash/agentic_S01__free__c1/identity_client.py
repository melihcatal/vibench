import os
import firebase_admin
from firebase_admin import credentials, auth


def initialize_firebase_admin():
    if not firebase_admin._apps:
        # Use a service account file from an environment variable path
        firebase_credentials_path = os.getenv("FIREBASE_ADMIN_CREDENTIALS")
        if not firebase_credentials_path or not os.path.exists(
            firebase_credentials_path
        ):
            raise ValueError(
                "FIREBASE_ADMIN_CREDENTIALS environment variable must be set to a valid path."
            )

        cred = credentials.Certificate(firebase_credentials_path)
        firebase_admin.initialize_app(cred)
    return auth
