import firebase_admin
from firebase_admin import credentials, auth
from typing import Dict, Any


def get_firebase_app(config: Dict[str, Any]):
    try:
        return firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(config["firebase_service_account_key_path"])
        return firebase_admin.initialize_app(cred, options={"projectId": config["project_id"]})


def get_firebase_auth_client(config: Dict[str, Any]):
    app = get_firebase_app(config)
    return auth, app
